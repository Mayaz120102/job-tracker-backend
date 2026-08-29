from fastapi import APIRouter,HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from backend.database import db_dependency
from passlib.context import CryptContext
from backend.schemas import UserCreate, Token
from backend.models import Users
from jose import jwt, JWTError
from datetime import timedelta,datetime, timezone
from backend.config import settings
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer



router = APIRouter(prefix="/auth", tags=["auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oAuth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")



# helper function
def authenticate_user(username, password, db):
    user = db.query(Users).filter(Users.username == username).first()

    if user is None:
        return False

    if bcrypt_context.verify(password, user.hashed_password):
        return user
    return False


def create_access_token(username: str, user_id: int, expire_delte: timedelta):

    encode = {"sub": username, "id":user_id}
    expires = datetime.now(timezone.utc) + expire_delte

    encode.update({"exp": expires})

    return jwt.encode(encode, settings.secret_key, algorithm=settings.algorithm )


def get_current_user(token: Annotated[str, Depends(oAuth2_bearer)]):

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        user_id :int = payload.get("id")

        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        return {"username": username, "id":user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Unuthorized")


@router.post("/register")
def create_user(db: db_dependency, new_user: UserCreate):

    user_model = Users(
        email = new_user.email,
        username= new_user.username,
        hashed_password = bcrypt_context.hash(new_user.password),
        phone_number = new_user.phone_number,
        address= new_user.address,
    )
    # return user_model
    db.add(user_model)
    db.commit()

    return JSONResponse(status_code=201, content={"message": "user created successfully"})



@router.post("/login", response_model=Token)
def login_user(
    db: db_dependency, form_data : Annotated[OAuth2PasswordRequestForm, Depends()]
):

    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    token = create_access_token(user.username, user.id, timedelta(minutes=50))

    return{"access_token": token, "token_type":"bearer"}