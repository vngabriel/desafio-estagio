export function getCookie(cookieName) {
    let token;

    document.cookie.split(";").forEach((cookie) => {
        cookie = cookie.split("=");
        if (cookie[0].trim() == cookieName) {
            token = cookie[1];
        }
    });

    return token;
}

export function setCookie(cookieName, value) {
    document.cookie = cookieName + "=" + value;
}

export function deleteCookie(cookieName) {
    document.cookie = cookieName + "=;";
}

export async function signup(userData) {
    return await postData("http://localhost:8000/api/signup/", 'application/json', userData);
}

export async function createAddress(addressData, userId) {
    return await postData(`http://localhost:8000/api/users/${userId}/address`, 'application/json', addressData)
}

export async function login(username, password) {
    return await postData("http://localhost:8000/api/login/", "application/x-www-form-urlencoded", {
        "username": username,
        "password": password
    });
}

export async function updateUser(userData, token) {
    return await putData("http://localhost:8000/api/users/", 'application/json', userData, token);
}

export async function updateAddress(addressData, token) {
    return await putData("http://localhost:8000/api/users/address/", 'application/json', addressData, token);
}

export async function deleteUser(token) {
    return await deleteData("http://localhost:8000/api/users/", token);
}

export async function postData(url, contentType, data) {
    let body;
    if (contentType === "application/x-www-form-urlencoded") {
        body = new URLSearchParams(data);
    } else {
        body = JSON.stringify(data);
    }

    const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': contentType
        },
        body: body
    });

    return response;
}

export async function putData(url, contentType, data, token) {
    let body;
    if (contentType === "application/x-www-form-urlencoded") {
        body = new URLSearchParams(data);
    } else {
        body = JSON.stringify(data);
    }

    const response = await fetch(url, {
        method: 'PUT',
        mode: 'cors',
        headers: {
          'Content-Type': contentType,
          'Authorization': `Bearer ${token}`
        },
        body: body
    });

    return response;
}

export async function deleteData(url, token) {

    const response = await fetch(url, {
        method: 'DELETE',
        mode: 'cors',
        headers: {
          'Authorization': `Bearer ${token}`
        }
    });

    return response;
}

export async function getData(url, token) {
    const response = await fetch(url, {
        method: 'GET',
        mode: 'cors',
        headers: {
          'Authorization': `Bearer ${token}`
        }
    });

    return response;
}

