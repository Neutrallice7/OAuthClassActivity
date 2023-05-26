from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime,timedelta
from jose import JWTError,jwt
from passlib.context import CryptContext
import uvicorn
from fastapi.middleware.cors import CORSMiddleware 


SECRET_KEY="83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

app=FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#need to connect to a database
db={
    "kevin":{
        "username":"kevin",
        "full_name":"Kevin Matthew Tanuwijaya",
        "email":"temp@gmail.com",
        "hashed_password":"$2b$12$UcSEzLndAX3jTb9S1kB4QOHVEdZRBdZg5fpPZNzHhHJOYGWsmuM2C",
        "disabled":False
    }
}

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:str or None=None

class User(BaseModel):
    username:str
    email:str or None=None
    full_name:str or None=None
    disabled:bool or None=None

class UserInDB(User):
    hashed_password:str


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth_2_scheme=OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hashed(password):
    return pwd_context.hash(password)

def get_user(db,username:str):
    if username in db:
        user_data=db[username]
        return UserInDB(**user_data)
    
def authenticate_user(db,username:str, password:str):
    user=get_user(db,username)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    
    return user

def create_access_token(data:dict,expires_delta:timedelta or None=None):
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.utcnow()+ expires_delta
    else:
        expire=datetime.utcnow()+timedelta(minutes=15)
    
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token:str=Depends(oauth_2_scheme)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials",headers={"WWW-authenticate":"bearer"})
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get("sub")
        if username is None:
            raise credential_exception
        token_data=TokenData(username=username)
    except JWTError:
        raise credential_exception
    
    #hold
    user=get_user(db,username=token_data.username)
    if user is None:
        raise credential_exception
    
    return user

async def get_current_active_user(current_user:UserInDB=Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400,detail="Inactive User")

    return current_user

@app.post("/token",response_model=Token)
async def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends()):
    user=authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="incorrect username or password",headers={"WWW-authenticate":"bearer"})
    
    access_token_expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token=create_access_token(data={"sub":user.username},expires_delta=access_token_expires)
    return{"access_token":access_token,"token_type":"bearer"}

@app.get("/users/me",response_model=User)
async def read_users_me(current_user:User=Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items",response_model=User)
async def read_own_items(current_user:User=Depends(get_current_active_user)):
    return [{"item_id":1,"owner":current_user}]

#Start server
uvicorn.run(app,host="0.0.0.0",port=8000)