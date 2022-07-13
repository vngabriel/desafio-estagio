import { getCookie, deleteCookie, getData } from "../services.js";


function checkAuthentication() {
    const accessToken = getCookie("access_token");

    getData("http://localhost:8000/api/user/", accessToken)
    .then(response => {
        if (!response.ok) {
            window.location = "index.html";
            sessionStorage.setItem("danger-msg", "Token expirado, por favor, realize o login novamente!");
        } else {
            return response.json();
        }
    })
    .then(json => {
        setTitle(json.name)
    })
    .catch(e => {
        window.location = "index.html";
        sessionStorage.setItem("danger-msg", "Token expirado, por favor, realize o login novamente!");
    });
}


function setTitle(userName) {
    document.getElementById("title").innerHTML = `Olá, ${userName}!`;
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

const form = document.getElementById("logout_form");

form.addEventListener("submit", (event) => {
    event.preventDefault();

    deleteCookie("access_token");
    deleteCookie("refresh_token");

    window.location = "index.html";
});
