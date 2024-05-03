import Page from "./Page.js";
import { signupInfo } from "./Info.js";

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
        this.$form.addEventListener("submit", async (event) => {
            event.preventDefault();
            try {
                signupInfo.sendData = {
                    email: this.$form.querySelector("#email").value,
                    password: this.$form.querySelector("#password").value,
                    username: this.$form.querySelector("#username").value,
                };
                await signupInfo.requestAPI();
                this.shift("login_page");
            }
            catch (e) {
                alert(`Signup: ${e.message}`);
            }
        });
    }
    
    init() {

    }

    fini() {
        this.$form.querySelector("#email").value = "";
        this.$form.querySelector("#password").value = "";
        this.$form.querySelector("#username").value = "";
    }
};
