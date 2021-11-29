import uvicorn
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List,Optional
from TWnews import news
from datetime import datetime,timedelta
from passlib.context import CryptContext

class News(BaseModel):
    #period: str=None
    keyword: str
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
class UserLogin(BaseException):
    username:str
    password:str

    class Config:
        schema_extra = {
            "example":{
                "username":"test",
                "password":"test"
            }
        }
class Token(BaseModel):
    access_token: str
    token_type: str
class UserInDB(User):
    hashed_password: str
class TokenData(BaseModel):
    username: Optional[str] = None

users = []
app = FastAPI()
SECRET_KEY = "0f89f4495cd141c00a9e3148f19ce21a54090a8b205d3523577bd4b273fbecbc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}
@app.get("/")
def root():
    jwt_encoded = jwt.encode({"some": "payload"}, SECRET_KEY, algorithm=ALGORITHM)
    return {"message": jwt_encoded}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db,username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post('/signup')    #Create User
def create_user(user:User):
    new_user = {
        "username":user.username,
        "email":user.email,
        "password":user.password
    }
    users.append(new_user)
    return new_user

@app.get('/users',response_model=List[User])
def get_users():
    return users
@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.get("/get_google_news")
async def get_google_news(item:News):
    return news().get_google_news(item.keyword)
@app.get("/get_udn_news")
async def get_udn_news(item:News):
    return news().get_udn_news(item.keyword)
@app.get("/get_apple_news")
async def get_apple_news(item:News):
    return news().get_apple_news(item.keyword)
@app.get("/get_setn_news")
async def get_setn_news(item:News):
    return news().get_setn_news(item.keyword)
@app.get("/get_ettoday_news")
async def get_ettoday_news(item:News):
    return news().get_ettoday_news(item.keyword)
@app.get("/get_TVBS_news")
async def get_TVBS_news(item:News):
    return news().get_TVBS_news(item.keyword)
@app.get("/get_china_news")
async def get_china_news(item:News):
    return news().get_china_news(item.keyword)
@app.get("/get_storm_news")
async def get_storm_news(item:News):
    return news().get_storm_news(item.keyword)
@app.get("/get_ttv_news")
async def get_ttv_news(item:News):
    return news().get_ttv_news(item.keyword)
@app.get("/get_ftv_news")
async def get_ftv_news(item:News):
    return news().get_ftv_news(item.keyword)
@app.get("/get_cna_news")
async def get_cna_news(item:News):
    return news().get_cna_news(item.keyword)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
