const $login = document.querySelector(".login-class");
const $signupBtn = document.querySelector("button");
const $signup = document.querySelector(".signup");
const $main = document.querySelector(".main");
$signupBtn.addEventListener("click", () => {
    $login.classList.add("none");
    $signupBtn.classList.add("none");
    $signup.classList.remove("none");
});

class Login {
    $loginForm;
    userId;

    constructor(login) {
        this.$loginForm = login;
        this.setEvent();
    }

    setEvent() {
        this.$loginForm.addEventListener("submit", (event) => {
            event.preventDefault();
            this.postLoginInfo({
                email: this.$loginForm.querySelector("input:first-child").value,
                password: this.$loginForm.querySelector("input:nth-child(2)").value
            });
        })
    }

    postLoginInfo = async (data) => {
        const response = await fetch("http://localhost:8000/api/login/", {
            method: "POST",
            headers: {
                "Host": "localhost:8000",
                "Origin": "http://localhost:5500",
                "Access-Control-Allow-Origin": "http://localhost:5500",
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data),
            credentials: "include"
        });

        if (!response.ok) {
            alert("`HTTP Error : ${response.status}`");
        }
        else {
            const res = await response.json();
            if (res.success) {
                this.inputId = res.data.username;
                this.$loginForm.classList.add("none");
                $main.classList.remove("none");
            }
            else
                alert("Wrong Id or Password!");
        }
    };
};

class Signup {
    $signup;

    constructor(signup) {
        this.$signup = signup;
        this.setEvent();
    }

    setEvent() {
        this.$signup.addEventListener("submit", (event) => {
            event.preventDefault();
            this.postSignupInfo({
                email: this.$signup.querySelector("input:first-child").value,
                password: this.$signup.querySelector("input:nth-child(2)").value,
                username: this.$signup.querySelector("input:nth-child(3)").value
            });
        });
    }

    postSignupInfo = async (data) => {
        const response = await fetch("http://localhost:8000/api/signup/", {
            method: "POST",
            headers: {
                "Host": "localhost:8000",
                "Origin": "http://localhost:5500",
                "Access-Control-Allow-Origin": "http://localhost:5500",
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data),
            credentials: "include"
        });

        if (!response.ok) {
            alert("`HTTP Error : ${response.status}`");
        }
        else {
            const res = await response.json();
            if (res.success) {
                this.$signup.classList.add("none");
                $main.classList.remove("none");
            }
            else
                alert("Wrong Id or Password!");
        }
    };
};

const login = new Login($login);
const signup = new Signup($signup);
