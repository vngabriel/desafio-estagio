from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    cpf = Column(String, unique=True)
    pis = Column(String, unique=True)
    hashed_password = Column(String)

    # uselist=False is needed to make one-to-one relationship
    address = relationship("Address", back_populates="resident", uselist=False, cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String)
    state = Column(String)
    city = Column(String)
    zip_code = Column(String)
    street = Column(String)
    number = Column(Integer)
    complement = Column(String, nullable=True)

    resident_id = Column(Integer, ForeignKey("users.id"))
    resident = relationship("User", back_populates="address")
