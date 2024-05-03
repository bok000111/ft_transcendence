import Page from "./Page.js";
import { loginInfo } from "./Info.js";

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
        this.$form.addEventListener("submit", async (event) => {
            event.preventDefault();
            try {
                loginInfo.sendData = {
                    email: this.$form.querySelector("#email").value,
                    password: this.$form.querySelector("#password").value,
                };
                await loginInfo.requestAPI();
                this.shift("main_page");
            }
            catch (e) {
                alert(`Login: ${e.message}`);
            }
        });
    }

    init() {

    }

    fini() {
        this.$form.querySelector("#email").value = "";
        this.$form.querySelector("#password").value = "";
    }
};
