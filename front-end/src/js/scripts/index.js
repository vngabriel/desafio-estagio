import { login, getCookie, setCookie, getData } from "../services.js";


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

let successMsg = sessionStorage.getItem("success-msg");
if (successMsg) {
    const successMsgDiv = document.getElementById("success-msg");
    successMsgDiv.innerHTML = successMsg;
    successMsgDiv.style.display = "block";
    sessionStorage.removeItem("success-msg");
}

let dangerMsg = sessionStorage.getItem("danger-msg");
if (dangerMsg) {
    const dangerMsgDiv = document.getElementById("danger-msg");
    dangerMsgDiv.innerHTML = dangerMsg;
    dangerMsgDiv.style.display = "block";
    sessionStorage.removeItem("danger-msg");
}

const form = document.getElementById("login_form");

form.addEventListener("submit", (event) => {
    event.preventDefault();
    document.getElementById("login-validation-msg").innerHTML = "";

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    login(username, password)
    .then(response => {
        if (response.ok) {
            return response.json();
        }
    })
    .then(json => {
        const accessToken = json.access_token;
        const refreshToken = json.refresh_token;

        setCookie("access_token", accessToken);
        setCookie("refresh_token", refreshToken);

        window.location = "user.html";
    })
    .catch(e => {
        document.getElementById("login-validation-msg").innerHTML = "Usuário ou senha incorretos.";
    });
});
