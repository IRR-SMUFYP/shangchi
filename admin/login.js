var user = ""

function checkLogin() {
    if (sessionStorage.getItem("user") != null) {
        user = JSON.parse(sessionStorage.getItem("user"))
        // console.log(JSON.parse(user))

        document.getElementById("loginLogoutButton").innerText = "Logout"
    }
}

function loginLogout() {
    if (document.getElementById("loginLogoutButton").innerText === "Login") {
        window.location.href = "login.html"
    } else {
        // user = ""
        sessionStorage.removeItem("user")
        if (window.location.href.includes("admin")) {
            window.location.href = "../index.html"
        } else {
            window.location.href = "index.html"
        }
    }
}
