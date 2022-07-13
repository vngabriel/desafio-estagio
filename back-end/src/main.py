from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime
from pydantic import ValidationError

from . import crud, models, schemas, utils
from .validation import validate_user_creation, validate_user_update
from .database import engine
from .dependencies import get_db, get_current_user, oauth2_scheme


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get('/', response_class=RedirectResponse, include_in_schema=False)
def docs():
    return RedirectResponse(url='/docs')


# using response_model=schemas.User will get the SQLAlchemy model data and put into Pydantic model to return the response
@app.post("/api/signup/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    validate_user_creation(db, user)

    return crud.create_user(db, user)


@app.post("/api/login/", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect information")

    hashed_password = user.hashed_password
    if not utils.verify_password(form_data.password, hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect information")

    return {
        "access_token": utils.create_access_token(user.email),
        "refresh_token": utils.create_refresh_token(user.email),
        "token_type": "bearer"
    }


@app.post('/api/token/refresh/')
def refresh(refresh_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(refresh_token, utils.JWT_SECRET_KEY, algorithms=[utils.ALGORITHM])
        token_data = schemas.TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    new_access_token = utils.create_access_token(token_data.sub)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": new_access_token})


@app.get('/api/user/', summary='Get details of currently logged user', response_model=schemas.User)
def read_user_with_token(user: models.User = Depends(get_current_user)):
    return user


@app.get('/api/users/{user_id}/', response_model=schemas.User)
def read_user_with_id(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    return user


@app.put("/api/users/", response_model=schemas.User)
def update_user(updated_user: schemas.UserUpdate, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    validate_user_update(db, updated_user, user)

    return crud.update_user(db, user, updated_user)


@app.delete("/api/users/")
def delete_user(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.delete_user(db, user)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "User deleted successfully"})


@app.post("/api/users/{user_id}/address/", response_model=schemas.Address)
def create_address_for_user(user_id: int, address: schemas.AddressCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if db_user.address:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already has address")
    return crud.create_address(db, address, user_id)


@app.get("/api/address/{address_id}", response_model=schemas.Address)
def read_address(address_id: int, db: Session = Depends(get_db)):
    db_address = crud.get_address(db, address_id)
    if db_address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return db_address


@app.put("/api/users/address/", response_model=schemas.Address)
def update_address(updated_address: schemas.AddressUpdate, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_address = crud.get_address(db, user.address.id)
    if db_address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return crud.update_address(db, db_address, updated_address)


@app.delete("/api/address/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = crud.get_address(db, address_id)
    if db_address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    crud.delete_address(db, db_address)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Address deleted successfully"})
