import { authPage } from "./AuthPage.js";
import { loginAPI } from "../../models/API.js";
import { info } from "../../models/Info.js";
import SubPage from "../SubPage.js";

class LoginSubpage extends SubPage {
    $form;
    $btn;

    init() {
        this.$elem.innerHTML = `
            <form>
                <input id="email" type="text" placeholder="email">
                <input id="password" type="password" placeholder="password">
                <input type="submit" value="login">
            </form>
            <button>signup</button>
        `;

        this.$form = this.$elem.querySelector("form");
        this.$btn = this.$elem.querySelector("button");

        this.$form.addEventListener("submit", async (event) => {
            event.preventDefault();
            loginAPI.sendData = {
                email: this.$form.querySelector("#email").value,
                password: this.$form.querySelector("#password").value,
            };
            try {
                await loginAPI.request();
                info.username = loginAPI.recvData.data.user.username;
                this.requestShift("main_page");
            }
            catch (e) {
                alert(`Login: ${e.message}`);
            }
        });

        this.$btn.addEventListener("click", () => {
            this.requestShift("signup_subpage");
        });
    }
    
    fini() {
        this.$elem.innerHTML = ``;
    }
};

export const loginSubpage = new LoginSubpage(
    authPage.$elem.querySelector("div"),
    authPage,
    null,
    "login_subpage"
);