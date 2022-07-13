from sqlalchemy.orm import Session

from . import models, schemas, utils


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_email_excluding_specific_user(db: Session, email: str, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id != user_id).filter(models.User.email == email).first()


def get_user_by_cpf(db: Session, cpf: str) -> models.User:
    return db.query(models.User).filter(models.User.cpf == cpf).first()


def get_user_by_cpf_excluding_specific_user(db: Session, cpf: str, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id != user_id).filter(models.User.cpf == cpf).first()


def get_user_by_pis(db: Session, pis: str) -> models.User:
    return db.query(models.User).filter(models.User.pis == pis).first()


def get_user_by_pis_excluding_specific_user(db: Session, pis: str, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id != user_id).filter(models.User.pis == pis).first()


def get_user_by_username(db: Session, username: str) -> models.User:
    db_user = get_user_by_email(db, username)
    if db_user is None:
        cpf = username.replace(".", "")
        cpf = cpf.replace("-", "")
        db_user = get_user_by_cpf(db, cpf)
    if db_user is None:
        pis = username.replace(".", "")
        pis = pis.replace("-", "")
        db_user = get_user_by_pis(db, pis)

    return db_user


def get_users(db: Session) -> list[models.User]:
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    cpf = user.cpf.replace(".", "")
    cpf = cpf.replace("-", "")
    pis = user.pis.replace(".", "")
    pis = pis.replace("-", "")
    hashed_password = utils.get_hashed_password(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        cpf=cpf,
        pis=pis,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(db: Session, db_user: models.User, updated_user: schemas.UserUpdate) -> models.User:
    cpf = updated_user.cpf
    pis = updated_user.pis
    if updated_user.cpf:
        cpf = cpf.replace(".", "")
        cpf = cpf.replace("-", "")
    if updated_user.pis:
        pis = pis.replace(".", "")
        pis = pis.replace("-", "")

    db_user.name = updated_user.name if updated_user.name else db_user.name
    db_user.email = updated_user.email if updated_user.email else db_user.email
    db_user.cpf = cpf if updated_user.cpf else db_user.cpf
    db_user.pis = pis if updated_user.pis else db_user.pis

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, db_user: models.User) -> None:
    db.delete(db_user)
    db.commit()


def get_address(db: Session, address_id: int) -> models.Address:
    return db.query(models.Address).filter(models.Address.id == address_id).first()


def create_address(db: Session, address: schemas.AddressCreate, user_id: int) -> models.Address:
    db_address = models.Address(
        **address.dict(),
        resident_id=user_id
    )
    db.add(db_address)
    db.commit()
    db.refresh(db_address)

    return db_address


def update_address(db: Session, db_address: models.Address, updated_address: schemas.AddressUpdate) -> models.Address:
    db_address.country = updated_address.country if updated_address.country else db_address.country
    db_address.state = updated_address.state if updated_address.state else db_address.state
    db_address.city = updated_address.city if updated_address.city else db_address.city
    db_address.zip_code = updated_address.zip_code if updated_address.zip_code else db_address.zip_code
    db_address.street = updated_address.street if updated_address.street else db_address.street
    db_address.number = updated_address.number if updated_address.number else db_address.number
    db_address.complement = updated_address.complement

    db.commit()
    db.refresh(db_address)

    return db_address


def delete_address(db: Session, db_address: models.Address) -> None:
    db.delete(db_address)
    db.commit()
