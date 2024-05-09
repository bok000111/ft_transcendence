import Page from "../Page.js";
import { loginInfo } from "../../models/Info.js";

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
            loginInfo.sendData = {
                email: this.$form.querySelector("#email").value,
                password: this.$form.querySelector("#password").value,
            };
            try {
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

// import { page_shifter } from "s;;;"
// const loginPage = new LoginPage(page_shifter, "login_page");

// const loginPage = new LoginPage(login_shifter, "login_sub_page");
