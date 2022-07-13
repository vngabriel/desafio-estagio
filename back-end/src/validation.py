from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from . import crud, schemas, models


def validate_user_creation(db: Session, user: schemas.UserCreate):
    cpf = user.cpf.replace(".", "")
    cpf = cpf.replace("-", "")
    pis = user.pis.replace(".", "")
    pis = pis.replace("-", "")

    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=[{"loc": ["body", "email"], "msg": "Email already registered"}])
    db_user = crud.get_user_by_cpf(db, cpf)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=[{"loc": ["body", "cpf"], "msg": "CPF already registered"}])
    db_user = crud.get_user_by_pis(db, pis)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=[{"loc": ["body", "pis"], "msg": "PIS already registered"}])


def validate_user_update(db: Session, updated_user: schemas.UserUpdate, user: models.User):
    db_user = crud.get_user_by_email_excluding_specific_user(db, updated_user.email, user.id)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"loc": ["body", "email"], "msg": "Email already registered"})
    db_user = crud.get_user_by_cpf_excluding_specific_user(db, updated_user.cpf, user.id)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"loc": ["body", "cpf"], "msg": "CPF already registered"})
    db_user = crud.get_user_by_pis_excluding_specific_user(db, updated_user.pis, user.id)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"loc": ["body", "pis"], "msg": "PIS already registered"})
