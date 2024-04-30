import Page from "./Page.js";

class SignupPage extends Page {
    $form;
    $button;

    setup() {
        this.mount("signup_page");
        this.$form = this.$elem.querySelector("form");
        this.$button = this.$elem.querySelector("button");
    }

    setEvent() {
        this.$button.addEventListener("click", () => {
            this.shift("login_page");
        });
        this.$form.addEventListener("submit", (event) => {
            event.preventDefault();
            this.postSignupInfo({
                email: this.$form.querySelector("[placeholder=email]").value,
                password: this.$form.querySelector("[placeholder=password]").value,
                username: this.$form.querySelector("[placeholder=username]").value,
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
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
            credentials: "include",
        });

        if (!response.ok) {
            alert(`HTTP Error : ${response.status}`);
        }
        else {
            const res = await response.json();
            if (res.success)
                this.shift("login_page");
            else
                alert("input is wrong!");
        }
    }

    init() {

    }

    fini() {
        this.$form.querySelector("[placeholder=email]").value = "";
        this.$form.querySelector("[placeholder=password]").value = "";
        this.$form.querySelector("[placeholder=username]").value = "";
    }
};
