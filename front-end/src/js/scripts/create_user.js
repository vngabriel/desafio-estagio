import { createAddress, signup, getCookie, getData } from "../services.js";
import { addErrorMessage, removerErrorMessage, validateAddressData } from "../validation.js";


function checkAuthentication() {
    const accessToken = getCookie("access_token");

    getData("http://localhost:8000/api/user/", accessToken)
    .then(response => {
        if (response.ok) {
            return response.json();
        }
    })
    .then(json => {
        if (json) {
            window.location = "user.html";
        }
    })
    .catch(e => {
        sessionStorage.setItem("danger-msg", "Token expirado, por favor, realize o login novamente!");
    }); 
}


checkAuthentication();

const form = document.getElementById("signup_form");

form.addEventListener("submit", (event) => {
    removerErrorMessage();
    event.preventDefault();

    const name = document.getElementById("name").value;
    const cpf = document.getElementById("cpf").value;
    const pis = document.getElementById("pis").value;
    const country = document.getElementById("country").value;
    const state = document.getElementById("state").value;
    const city = document.getElementById("city").value;
    const zipcode = document.getElementById("zipcode").value;
    const street = document.getElementById("street").value;
    const number = document.getElementById("number").value;
    const complement = document.getElementById("complement").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmation_password = document.getElementById("confirmation_password").value;

    const userData = {
        "name": name,
        "email": email,
        "cpf": cpf,
        "pis": pis,
        "password": password,
        "confirmation_password": confirmation_password
    };

    const addressData = {
        "country": country,
        "state": state,
        "city": city,
        "zip_code": zipcode,
        "street": street,
        "number": number,
        "complement": complement
    };

    if (validateAddressData(addressData)) {
        signup(userData)
        .then(response => {
            return response.json();
        })
        .then(json => {
            if (json.hasOwnProperty("detail")) {
                json.detail.forEach(error => {
                    addErrorMessage(error.loc[1])
                });
            } else {
                createAddress(addressData, json.id)
                .then(response => {
                    return response.json();
                })
                .then(json => {
                    if (json.hasOwnProperty("detail")) {
                        json.detail.forEach(error => {
                            addErrorMessage(error.loc[1])
                        });
                    } else {
                        window.location = "index.html";
                        sessionStorage.setItem("success-msg", "Conta criada com sucesso!");
                    }
                })
                .catch(e => {
                    const dangerMsgDiv = document.getElementById("danger-msg");
                    dangerMsgDiv.innerHTML = "Erro na criação do endereço!";
                    dangerMsgDiv.style.display = "block";
                });
            }
        })
        .catch(e => {
            const dangerMsgDiv = document.getElementById("danger-msg");
            dangerMsgDiv.innerHTML = "Erro na criação do usuário!";
            dangerMsgDiv.style.display = "block";
        });
    }

});