from typing import Union
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm

import services as _services
import schemas as _schemas

from fastapi.middleware.cors import CORSMiddleware

import uvicorn

app = _fastapi.FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# POST request that creates a new user.
@app.post("/api/users")
async def create_user(
    user: _schemas.userCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code = 400, detail = "Email already in use")

    user = await _services.create_user(user, db)

    return await _services.create_token(user)

# POST request that generates a token for an existing user. 
@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)
 
    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")
 
    return await _services.create_token(user)

# GET request that retrieves the profile of the currently authenticated user.
@app.get("/api/users/myprofile", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user

#Start server

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)