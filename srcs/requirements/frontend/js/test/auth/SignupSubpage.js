import { auth } from "../Page.js";
import { signupInfo } from "../../models/Info.js";
import SubPage from "../SubPage.js";

class SignupSubpage extends SubPage {
    $form;
    $btn;

    init() {
        this.$elem.innerHTML = `
            <form>
                <input id="email" type="text" placeholder="email">
                <input id="password" type="text" placeholder="password">
                <input id="username" type="text" placeholder="username">
                <input type="submit" value="signup">
            </form>
            <button>signup</button>
        `;

        this.$form = this.$elem.querySelector("form");
        this.$btn = this.$elem.querySelector("button");

        this.$form.addEventListener("submit", async (event) => {
            event.preventDefault();
            signupInfo.sendData = {
                email: this.$form.querySelector("#email").value,
                password: this.$form.querySelector("#password").value,
                username: this.$form.querySelector("#username").value,
            };
            try {
                await signupInfo.requestAPI();
                this.requestShift("login_subpage");
            }
            catch (e) {
                alert(`Signup: ${e.message}`);
            }
        });

        this.$btn.addEventListener("click", () => {
            this.requestShift("login_subpage");
        });
    }

    fini() {
        this.$elem.innerHTML = ``;
    }
};

const signupSubpage = new SignupSubpage(
    auth.$elem.querySelector("div"),
    auth,
    null,
    "signup_subpage"
);