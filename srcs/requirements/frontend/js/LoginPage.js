import Page from "./Page.js";
import Component from "./Component.js";

class Login extends Component {
    $email;
    $password;

    setup() {
        this.$email = this.$elem.querySelector("[placeholder=email]");
        this.$password = this.$elem.querySelector("[placeholder=password]");
    }

    setEvent() {
        this.$elem.addEventListener("submit", (event) => {
            event.preventDefault();
            this.postLoginInfo({
                email: this.$email.value,
                password: this.$password.value,
            });
        });
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
            alert(`HTTP Error : ${response.status}`);
        }
        else {
            const res = await response.json();
            if (res.success) {
                this.inputId = res.data.username;
                this.$elem.classList.add("none");
                $main.classList.remove("none");
            }
            else
                alert("Wrong Id or Password!");
        }
    };
};

class Signup extends Component {
    $email;
    $password;
    $username;

    setup() {
        this.$email = this.$elem.querySelector("[placeholder=email]");
        this.$password = this.$elem.querySelector("[placeholder=password]");
        this.$username = this.$elem.querySelector("[placeholder=username]");
    }

    setEvent() {
        this.$elem.addEventListener("submit", (event) => {
            event.preventDefault();
            this.postSignupInfo({
                email: this.$email.value,
                password: this.$password.value,
                username: this.$username.value,
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
            alert(`HTTP Error : ${response.status}`);
        }
        else {
            const res = await response.json();
            if (res.success) {
                this.$elem.classList.add("none");
                $main.classList.remove("none");
            }
            else
                alert("Wrong Id or Password!");
        }
    };
}

class Switch extends Component {
    $login;
    $signup;

    setup() {
        this.$login = this.$elem.querySelector("button:first-child");
        this.$signup = this.$elem.querySelector("button:last-child");
    }

    setEvent() {
        this.$login.addEventListener("click", () => {
           // 수정중... 
           // 렌더링을 수행해야 하는데 여기서 하는게 맞나..?
        });
    }
}

class LoginPage extends Page {
    #login;
    #signup;
    #switch;

    setup() {
        this.#login = new Login(this.$elem.querySelector(".login"));
        this.#signup = new Signup(this.$elem.querySelector(".signup"));
        this.#switch = new Switch(this.$elem.querySelector(".switch"));
    }
    setEvent() {
        this.$signupBtn.addEventListener("click", () => {
            this.$signupBtn.classList.add("none");
            this.$loginForm.classList.add("none");
            this.$signupForm.classList.remove("none");
        });
        this.$loginForm.addEventListener("submit", (event) => {
            event.preventDefault();
            this.postLoginInfo({
                email: this.$loginForm.querySelector("input:first-child").value,
                password: this.$loginForm.querySelector("input:nth-child(2)").value,
            });
        });
    }
    init() {

    }
    fini() {

    }
};
