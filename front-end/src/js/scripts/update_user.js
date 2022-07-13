import { getCookie, getData, updateAddress, updateUser, deleteUser } from "../services.js";
import { addErrorMessage, removerErrorMessage, validateAddressData } from "../validation.js";


async function checkAuthentication() {
    const accessToken = getCookie("access_token");

    return await getData("http://localhost:8000/api/user/", accessToken)
}


const inputName = document.getElementById("name");
const inputCpf = document.getElementById("cpf");
const inputPis = document.getElementById("pis");
const inputCountry = document.getElementById("country");
const inputState = document.getElementById("state");
const inputCity = document.getElementById("city");
const inputZipcode = document.getElementById("zipcode");
const inputStreet = document.getElementById("street");
const inputNumber = document.getElementById("number");
const inputComplement = document.getElementById("complement");
const inputEmail = document.getElementById("email");


checkAuthentication()
.then(response => {
    if (response.ok) {
        return response.json();
    }
})
.then(user => {
    inputName.value = user.name;
    inputCpf.value = user.cpf;
    inputPis.value = user.pis;
    inputEmail.value = user.email;
    if (user.address) {
        inputCountry.value = user.address.country;
        inputState.value = user.address.state;
        inputCity.value = user.address.city;
        inputZipcode.value = user.address.zip_code;
        inputStreet.value = user.address.street;
        inputNumber.value = user.address.number;
        if (user.address.complement) {
            inputComplement.value = user.address.complement;
        }
    }
})
.catch(e => {
    window.location = "index.html";
    sessionStorage.setItem("danger-msg", "Token expirado, por favor, realize o login novamente!");
});

const updateForm = document.getElementById("update_form");
updateForm.addEventListener("submit", (event) => {
    event.preventDefault();
    removerErrorMessage();

    const userData = {
        "name": inputName.value,
        "email": inputEmail.value,
        "cpf": inputCpf.value,
        "pis": inputPis.value,
    };

    const addressData = {
        "country": inputCountry.value,
        "state": inputState.value,
        "city": inputCity.value,
        "zip_code": inputZipcode.value,
        "street": inputStreet.value,
        "number": inputNumber.value,
        "complement": inputComplement.value
    };

    const accessToken = getCookie("access_token");

    if (validateAddressData(addressData)) {
        updateUser(userData, accessToken)
        .then(response => {
            return response.json();
        })
        .then(json => {
            if (json.hasOwnProperty("detail")) {
                json.detail.forEach(error => {
                    addErrorMessage(error.loc[1])
                });
            } else {
                updateAddress(addressData, accessToken)
                .then(response => {
                    return response.json();
                })
                .then(json => {
                    if (json.hasOwnProperty("detail")) {
                        json.detail.forEach(error => {
                            addErrorMessage(error.loc[1])
                        });
                    } else {
                        window.location = "user.html";
                        sessionStorage.setItem("success-msg", "Conta atualizada com sucesso!");
                    }
                })
                .catch(e => {
                    const dangerMsgDiv = document.getElementById("danger-msg");
                    dangerMsgDiv.innerHTML = "Erro na atualização do endereço!";
                    dangerMsgDiv.style.display = "block";
                });
            }
        })
        .catch(e => {
            const dangerMsgDiv = document.getElementById("danger-msg");
            dangerMsgDiv.innerHTML = "Erro na atualização do usuário!";
            dangerMsgDiv.style.display = "block";
        });
    }

})

const deleteForm = document.getElementById("delete_form");
deleteForm.addEventListener("submit", (event) => {
    event.preventDefault();

    deleteUser(getCookie("access_token"))
    .then(response => {
        if (response.ok) {
            window.location = "index.html";
            sessionStorage.setItem("success-msg", "Conta excluída com sucesso!");
        }
    })
    .catch(e => {
        const dangerMsgDiv = document.getElementById("danger-msg");
        dangerMsgDiv.innerHTML = "Erro na exclusão do usuário!";
        dangerMsgDiv.style.display = "block";
    });
});