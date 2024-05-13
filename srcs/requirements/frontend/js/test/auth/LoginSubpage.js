import { auth } from "../Page.js";
import { loginInfo } from "../../models/Info.js";
import SubPage from "../SubPage.js";

class LoginSubpage extends SubPage {
    $form;
    $btn;

    init() {
        this.$elem.innerHTML = `
            <form>
                <input id="email" type="text" placeholder="email">
                <input id="password" type="text" placeholder="password">
                <input type="submit" value="login">
            </form>
            <button>signup</button>
        `;

        this.$form = this.$elem.querySelector("form");
        this.$btn = this.$elem.querySelector("button");

        this.$form.addEventListener("submit", async (event) => {
            event.preventDefault();
            loginInfo.sendData = {
                email: this.$form.querySelector("#email").value,
                password: this.$form.querySelector("#password").value,
            };
            try {
                await loginInfo.requestAPI();
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

const loginSubpage = new LoginSubpage(
    auth.$elem.querySelector("div"),
    auth,
    null,
    "login_subpage"
);