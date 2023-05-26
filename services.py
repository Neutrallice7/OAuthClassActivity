import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import sqlalchemy.orm as _orm
import passlib.hash as _hash

import database as _database
import models as _models
import schemas as _schemas

oauth2scheme = _security.OAuth2PasswordBearer(tokenUrl = "/api/token")

JWT_SECRET = "mochicheriecimolmomo"

def create_database():
    return _database.Base.metadata.create_all(bind = _database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

create_database()

async def create_user(user: _schemas.userCreate, db: _orm.Session):
    user_obj = _models.User(
        email = user.email, 
        hashed_password = _hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()

async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(db = db, email = email)
 
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user

async def create_token(user: _models.User):
    user_obj = _schemas.User.from_orm(user)

    token = _jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token = token, token_type = "bearer")

async def get_current_user(
    db: _orm.Session = _fastapi.Depends(get_db),
    token: str = _fastapi.Depends(oauth2scheme),
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code = 401, detail = "Invalid Email or Password"
        )
 
    return _schemas.User.from_orm(user)