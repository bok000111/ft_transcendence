import Page from "./Page.js";

/**
 * 성공 시 어떤 정보를 수신하고 저장해야 하는지에 대한 논의 필요.
 * Login 클래스가 그 정보를 저장하는 역할을 한다.
 * 정보를 저장하는 클래스는 Component와 별개로 동작.
 */
class Login {
    #username;
};

class LoginPage extends Page {
    $form;
    $button;

    setup() {
        this.mount("login_page");
        this.$form = this.$elem.querySelector("form");
        this.$button = this.$elem.querySelector("button");
    }

    setEvent() {
        this.$button.addEventListener("click", () => {
            this.shift("signup_page");
        });
        this.$form.addEventListener("submit", (event) => {
            event.preventDefault();
            this.postLoginInfo({
                email: this.$form.querySelector("[placeholder=email]").value,
                password: this.$form.querySelector("[placeholder=password]").value,
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
            if (res.success) {
                this.inputId = res.data.username; // 수정 필요.
                this.shift("main_page");
            }
            else
                alert("Wrong Id or Password!");
        }
    }

    init() {

    }

    fini() {
        this.$form.querySelector("[placeholder=email]").value = "";
        this.$form.querySelector("[placeholder=password]").value = "";
    }
};
