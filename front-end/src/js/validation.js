export function addErrorMessage(inputId) {
    let msg = "";
    if (inputId == "name") {
        msg = "Nome deve conter entre 3 e 100 letras."
    } else if (inputId == "cpf") {
        msg = "CPF inválido ou já cadastrado."
    } else if (inputId == "pis") {
        msg = "PIS inválido ou já cadastrado."
    } else if (inputId == "country") {
        msg = "País deve ter até 50 letras."
    } else if (inputId == "state") {
        msg = "Estado deve ter até 50 letras."
    } else if (inputId == "city") {
        msg = "Cidade deve ter até 50 letras."
    } else if (inputId == "zipcode") {
        msg = "CEP deve ter até 10 dígitos."
    } else if (inputId == "street") {
        msg = "Rua deve ter até 50 letras."
    } else if (inputId == "number") {
        msg = "Número não pode ser negativo."
    } else if (inputId == "complement") {
        msg = "Complemento deve conter até 250 letras."
    } else if (inputId == "email") {
        msg = "Email inválido ou já cadastrado."
    } else if (inputId == "password") {
        msg = "Senha inválida."
    } else if (inputId == "confirmation_password") {
        msg = "As senhas devem ser idênticas."
    }

    document.getElementById(`${inputId}-validation-msg`).innerHTML = msg;
}

export function removerErrorMessage() {
    document.getElementById("name-validation-msg").innerHTML = "";
    document.getElementById("cpf-validation-msg").innerHTML = "";
    document.getElementById("pis-validation-msg").innerHTML = "";
    document.getElementById("country-validation-msg").innerHTML = "";
    document.getElementById("state-validation-msg").innerHTML = "";
    document.getElementById("city-validation-msg").innerHTML = "";
    document.getElementById("zipcode-validation-msg").innerHTML = "";
    document.getElementById("street-validation-msg").innerHTML = "";
    document.getElementById("number-validation-msg").innerHTML = "";
    document.getElementById("complement-validation-msg").innerHTML = "";
    document.getElementById("email-validation-msg").innerHTML = "";
    const passwordInput = document.getElementById("password-validation-msg");
    if (passwordInput) {
        passwordInput.innerHTML = "";
    }
    const confirmPasswordInput = document.getElementById("confirmation_password-validation-msg");
    if (confirmPasswordInput) {
        confirmPasswordInput.innerHTML = "";
    }
}

export function validateAddressData(addressData) {
    if (addressData.country.length > 50) { 
        addErrorMessage("country");
        return false;
    } else if (addressData.state.length > 50) {
        addErrorMessage("state");
        return false;
    } else if (addressData.city.length > 50) {
        addErrorMessage("city");
        return false;
    } else if (addressData.zip_code.length > 10) {
        addErrorMessage("zipcode");
        return false;
    } else if (addressData.street.length > 50) {
        addErrorMessage("street");
        return false;
    } else if (addressData.number < 0) {
        addErrorMessage("number");
        return false;
    } else if (addressData.complement.length > 250) {
        addErrorMessage("complement");
        return false;
    }

    return true;
}