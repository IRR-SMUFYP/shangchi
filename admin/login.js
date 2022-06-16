var user = ""

function checkLogin() {
    if (sessionStorage.getItem("user") != null) {
        user = JSON.parse(sessionStorage.getItem("user"))
        // console.log(JSON.parse(user))

        document.getElementById("loginLogoutButton").innerText = "Logout"
    }
}

function checkAdmin() {
    if (sessionStorage.getItem("user") != null && ["admin","master"].includes(JSON.parse(sessionStorage.getItem("user")).userType)) {
        user = JSON.parse(sessionStorage.getItem("user"))
        // console.log(user)

        document.getElementById("loginLogoutButton").innerText = "Logout"
    } else {
        let confirmMsg = confirm(
            "Only Admins who are logged in have access to this page. Please log in before accessing this page."
            )
        if (confirmMsg) {
            window.location.href = "../login.html"
        } else {
            window.location.href = "../index.html"
        }
    }
}

function checkDriver() {
    if (sessionStorage.getItem("user") != null && ["driver"].includes(JSON.parse(sessionStorage.getItem("user")).userType)) {
        user = JSON.parse(sessionStorage.getItem("user"))
        // console.log(user)

        document.getElementById("loginLogoutButton").innerText = "Logout"
    } else {
        let confirmMsg = confirm(
            "Only Drivers who are logged in have access to this page. Please log in before accessing this page."
            )
        if (confirmMsg) {
            window.location.href = "../login.html"
        } else {
            window.location.href = "../index.html"
        }
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
        } 
        else if (window.location.href.includes("driver")) {
            window.location.href = "../index.html"
        } else {
            window.location.href = "index.html"
        }
    }
}
