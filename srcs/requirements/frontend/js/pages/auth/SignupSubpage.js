import { authPage } from "./AuthPage.js";
import { signupAPI } from "../../models/API.js";
import SubPage from "../SubPage.js";

class SignupSubpage extends SubPage {
    $form;
    $btn;

    init() {
        this.$elem.innerHTML = `
            <form>
                <input id="email" type="text" placeholder="email">
                <input id="password" type="password" placeholder="password">
                <input id="username" type="text" placeholder="username">
                <input type="submit" value="signup">
            </form>
            <button>login</button>
        `;

        this.$form = this.$elem.querySelector("form");
        this.$btn = this.$elem.querySelector("button");

        this.$form.addEventListener("submit", async (event) => {
            event.preventDefault();
            signupAPI.sendData = {
                email: this.$form.querySelector("#email").value,
                password: this.$form.querySelector("#password").value,
                username: this.$form.querySelector("#username").value,
            };
            try {
                await signupAPI.request();
                alert("Signup Success!");
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

export const signupSubpage = new SignupSubpage(
    authPage.$elem.querySelector("div"),
    authPage,
    null,
    "signup_subpage"
);