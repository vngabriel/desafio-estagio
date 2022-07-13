from fastapi.testclient import TestClient
from validate_docbr import CPF, PIS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from .main import app, get_db
from .database import Base
from .utils import create_access_token


load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_TEST_URL")
if os.path.exists(os.path.abspath(SQLALCHEMY_DATABASE_URL.split('/')[-1])):
    os.remove(os.path.abspath(SQLALCHEMY_DATABASE_URL.split('/')[-1]))

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_default_user_and_address():
    email = "test@example.com"
    cpf = "570.040.060-00"
    pis = "360.73636.92-5"

    response = client.post(
        "/api/signup/",
        headers={"Content-Type": "application/json"},
        json={
            "name": "Test Name",
            "email": email,
            "cpf": cpf,
            "pis": pis,
            "password": "testpassword",
            "confirmation_password": "testpassword"
        }
    )
    data = response.json()

    client.post(
        f"/api/users/{data['id']}/address/",
        headers={"Content-Type": "application/json"},
        json={
            "country": "País",
            "state": "Estado",
            "city": "Cidade",
            "zip_code": "55000000",
            "street": "Rua",
            "number": 10,
            "complement": "Complemento",
        }
    )


def create_user_without_address():
    email = generate_email()
    cpf = CPF().generate(False)
    pis = PIS().generate(False)

    response = client.post(
        "/api/signup/",
        headers={"Content-Type": "application/json"},
        json={
            "name": "Test Name",
            "email": email,
            "cpf": cpf,
            "pis": pis,
            "password": "testpassword",
            "confirmation_password": "testpassword"
        }
    )

    return response


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

create_default_user_and_address()


def generate_email():
    url = "https://emailfake.com/"

    email_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    email_driver.get(url)
    email_driver.maximize_window()

    email = email_driver.find_element(value="email_ch_text").text

    return email


def test_signup():
    email = generate_email()
    cpf = CPF().generate(False)
    pis = PIS().generate(False)

    response = client.post(
        "/api/signup/",
        headers={"Content-Type": "application/json"},
        json={
            "name": "Test Name",
            "email": email,
            "cpf": cpf,
            "pis": pis,
            "password": "testpassword",
            "confirmation_password": "testpassword"
        }
    )
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["name"] == "Test Name"
    assert data["email"] == email
    assert data["cpf"] == cpf
    assert data["pis"] == pis
    assert "id" in data

    user_id = data["id"]
    response = client.get(f"/api/users/{user_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Name"
    assert data["email"] == email
    assert data["cpf"] == cpf
    assert data["pis"] == pis
    assert data["id"] == user_id


def test_signup_with_email_already_registered():
    email = "test@example.com"
    cpf = CPF().generate(False)
    pis = PIS().generate(False)

    response = client.post(
        "/api/signup/",
        headers={"Content-Type": "application/json"},
        json={
            "name": "Test Name",
            "email": email,
            "cpf": cpf,
            "pis": pis,
            "password": "testpassword",
            "confirmation_password": "testpassword"
        }
    )
    assert response.status_code == 400, response.text


def test_signup_with_cpf_already_registered():
    email = generate_email()
    cpf = "570.040.060-00"
    pis = PIS().generate(False)

    response = client.post(
        "/api/signup/",
        headers={"Content-Type": "application/json"},
        json={
            "name": "Test Name",
            "email": email,
            "cpf": cpf,
            "pis": pis,
            "password": "testpassword",
            "confirmation_password": "testpassword"
        }
    )
    assert response.status_code == 400, response.text


def test_signup_with_pis_already_registered():
    email = generate_email()
    cpf = CPF().generate(False)
    pis = "360.73636.92-5"

    response = client.post(
        "/api/signup/",
        headers={"Content-Type": "application/json"},
        json={
            "name": "Test Name",
            "email": email,
            "cpf": cpf,
            "pis": pis,
            "password": "testpassword",
            "confirmation_password": "testpassword"
        }
    )
    assert response.status_code == 400, response.text


def test_signup_with_invalid_email():
    email = "invalidemail.com"
    cpf = CPF().generate(False)
    pis = PIS().generate(False)

    response = client.post(
        "/api/signup/",
        headers={"Content-Type": "application/json"},
        json={
            "name": "Test Name",
            "email": email,
            "cpf": cpf,
            "pis": pis,
            "password": "testpassword",
            "confirmation_password": "testpassword"
        }
    )
    assert response.status_code == 422, response.text


def test_signup_with_invalid_cpf():
    email = generate_email()
    cpf = "99999999999"
    pis = PIS().generate(False)

    response = client.post(
        "/api/signup/",
        headers={"Content-Type": "application/json"},
        json={
            "name": "Test Name",
            "email": email,
            "cpf": cpf,
            "pis": pis,
            "password": "testpassword",
            "confirmation_password": "testpassword"
        }
    )
    assert response.status_code == 422, response.text


def test_signup_with_invalid_pis():
    email = generate_email()
    cpf = CPF().generate(False)
    pis = "1111111111"

    response = client.post(
        "/api/signup/",
        headers={"Content-Type": "application/json"},
        json={
            "name": "Test Name",
            "email": email,
            "cpf": cpf,
            "pis": pis,
            "password": "testpassword",
            "confirmation_password": "testpassword"
        }
    )
    assert response.status_code == 422, response.text


def test_read_user():
    response = client.get(f"/api/users/{1}/")
    assert response.status_code == 200, response.text

    data = response.json()
    access_token = create_access_token(data["email"])

    response = client.get(
        "/api/user/",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200, response.text
    assert response.json()["id"] == data["id"], response.text


def test_read_user_with_invalid_token():
    access_token = "invalidtoken"
    response = client.get(
        "/api/user/",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 403, response.text


def test_read_user_with_expired_token():
    response = client.get(f"/api/users/{1}/")
    assert response.status_code == 200, response.text

    data = response.json()
    access_token = create_access_token(data["email"], 0)

    response = client.get(
        "/api/user/",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 401, response.text


def test_update_user():
    response = client.get(f"/api/users/{1}/")
    assert response.status_code == 200, response.text

    data = response.json()
    access_token = create_access_token(data["email"])

    cpf = CPF().generate(False)

    response = client.put(
        "/api/users/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "name": "Test Name Update",
            "cpf": cpf
        }
    )
    assert response.status_code == 200, response.text


def test_update_user_with_invalid_token():
    access_token = "invalidtoken"

    cpf = CPF().generate(False)

    response = client.put(
        "/api/users/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "name": "Test Name Update",
            "cpf": cpf
        }
    )
    assert response.status_code == 403, response.text


def test_delete_user():
    response = create_user_without_address()
    assert response.status_code == 200, response.text

    data = response.json()
    access_token = create_access_token(data["email"])

    response = client.delete(
        "/api/users/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200, response.text
    assert response.json() == {"detail": "User deleted successfully"}, response.text

    response = client.get(f"/api/users/{data['id']}/")
    assert response.status_code == 404, response.json()


def test_create_address():
    response = create_user_without_address()
    assert response.status_code == 200, response.text

    data = response.json()

    response = client.post(
        f"/api/users/{data['id']}/address/",
        headers={"Content-Type": "application/json"},
        json={
            "country": "País",
            "state": "Estado",
            "city": "Cidade",
            "zip_code": "55000000",
            "street": "Rua",
            "number": 10,
            "complement": "Complemento",
        }
    )

    assert response.status_code == 200, response.text


def test_create_address_for_user_already_with_address():
    response = client.post(
        "/api/users/1/address/",
        headers={"Content-Type": "application/json"},
        json={
            "country": "País",
            "state": "Estado",
            "city": "Cidade",
            "zip_code": "55000000",
            "street": "Rua",
            "number": 10,
            "complement": "Complemento",
        }
    )

    assert response.status_code == 400, response.text


def test_create_address_with_invalid_number():
    response = create_user_without_address()
    assert response.status_code == 200, response.text

    data = response.json()

    response = client.post(
        f"/api/users/{data['id']}/address/",
        headers={"Content-Type": "application/json"},
        json={
            "country": "País",
            "state": "Estado",
            "city": "Cidade",
            "zip_code": "55000000",
            "street": "Rua",
            "number": -10,
            "complement": "Complemento",
        }
    )

    assert response.status_code == 422, response.text


def test_create_address_with_invalid_user_id():
    response = client.post(
        "/api/users/0/address/",
        headers={"Content-Type": "application/json"},
        json={
            "country": "País",
            "state": "Estado",
            "city": "Cidade",
            "zip_code": "55000000",
            "street": "Rua",
            "number": 10,
            "complement": "Complemento",
        }
    )

    assert response.status_code == 404, response.text


def test_update_address():
    response = client.get(f"/api/users/{1}/")
    assert response.status_code == 200, response.text

    data = response.json()
    access_token = create_access_token(data["email"])

    response = client.put(
        "/api/users/address/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "country": "País Update",
            "state": "Estado Update",
            "city": "Cidade",
            "zip_code": "55000000",
            "street": "Rua Update",
            "number": 10,
            "complement": "Complemento Update",
        }
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["country"] == "País Update", response.text
    assert data["state"] == "Estado Update", response.text
    assert data["street"] == "Rua Update", response.text
    assert data["complement"] == "Complemento Update", response.text


def test_update_address_with_invalid_token():
    access_token = "invalidtoken"

    response = client.put(
        "/api/users/address/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "country": "País Update",
            "state": "Estado Update",
            "city": "Cidade",
            "zip_code": "55000000",
            "street": "Rua Update",
            "number": 10,
            "complement": "Complemento Update",
        }
    )

    assert response.status_code == 403, response.text
