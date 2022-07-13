from typing import Optional

from pydantic import BaseModel, validator, constr, EmailStr, NonNegativeInt
from validate_docbr import CPF, PIS


# Address
class AddressBase(BaseModel):
    country: constr(max_length=50)
    state: constr(max_length=50)
    city: constr(max_length=50)
    zip_code: constr(max_length=10)
    street: constr(max_length=50)
    number: NonNegativeInt
    complement: Optional[constr(max_length=250)] = None


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    country: Optional[constr(max_length=50)] = None
    state: Optional[constr(max_length=50)] = None
    city: Optional[constr(max_length=50)] = None
    zip_code: Optional[constr(max_length=10)] = None
    street: Optional[constr(max_length=50)] = None
    number: Optional[NonNegativeInt] = None
    complement: Optional[constr(max_length=250)] = None


class Address(AddressBase):
    id: int
    resident_id: int

    class Config:
        orm_mode = True


# User
class UserBase(BaseModel):
    name: constr(min_length=3, max_length=100)
    email: EmailStr
    cpf: str
    pis: str

    @validator('name')
    def name_must_contain_at_least_3_characters(cls, v):
        if len(v) < 3:
            raise ValueError("Must contain at least 3 characters.")
        if len(v) > 100:
            raise ValueError("Must contain a maximum of 100 characters.")
        return v.title()

    @validator('cpf')
    def cpf_validation(cls, v):
        cpf_validator = CPF()
        if not cpf_validator.validate(v):
            raise ValueError("Invalid CPF.")
        else:
            return v

    @validator('pis')
    def pis_validation(cls, v):
        pis_validator = PIS()
        if not pis_validator.validate(v):
            raise ValueError("Invalid PIS.")
        else:
            return v


class UserCreate(UserBase):
    password: str
    confirmation_password: str

    @validator('confirmation_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match.')
        return v


class UserUpdate(BaseModel):
    name: Optional[constr(min_length=3, max_length=100)] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str]
    pis: Optional[str]

    @validator('name')
    def name_must_contain_at_least_3_characters(cls, v):
        if len(v) < 3:
            raise ValueError('Must contain at least 3 characters.')
        return v.title()

    @validator('cpf')
    def cpf_validation(cls, v):
        cpf_validator = CPF()
        if not cpf_validator.validate(v):
            raise ValueError("Invalid CPF.")
        else:
            return v

    @validator('pis')
    def pis_validation(cls, v):
        pis_validator = PIS()
        if not pis_validator.validate(v):
            raise ValueError("Invalid PIS.")
        else:
            return v


class User(UserBase):
    id: int
    address: Optional[Address] = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
