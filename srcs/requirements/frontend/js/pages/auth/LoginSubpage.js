import { authPage } from "./AuthPage.js";
import { loginAPI } from "../../models/API.js";
import { info } from "../../models/Info.js";
import SubPage from "../SubPage.js";
import RootPage from "../RootPage.js"

class LoginSubpage extends SubPage {
    $form;
    $oauthbtn;
    $loginbtn;
    $signupbtn;
    response;

    init() {
        this.$elem.innerHTML = `
            <div class="container z_highest">
                <div class="row justify-content-center mt-5">
                    <div class="col-md-6 col-lg-4">
                        <h3 class="text-center">Login</h3>
                        <form>
                            <div class="mb-3 mt-4">
                                <label for="email" class="form-label">Email</label>
                                <input type="email" class="form-control" id="email" placeholder="Enter your email">
                            </div>
                            <div class="mb-3 mt-4">
                                <label for="password" class="form-label">Password</label>
                                <input type="password" class="form-control" id="password" placeholder="Enter your password">
                            </div>
                            <div class="mb-3 mt-4 d-grid gap-2">
                                <button type="submit" class="btn btn-primary" id="loginbtn">Login</button>
                                <button type="button" class="btn btn-primary" id="oauthbtn">Login with 42</button>
                                <button type="button" class="btn btn-secondary" id="signupbtn">Sign Up</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        `;

        this.$form = this.$elem.querySelector("form");
        this.$loginbtn = this.$elem.querySelector("#loginbtn");
        this.$signupbtn = this.$elem.querySelector("#signupbtn");
        this.$oauthbtn = this.$elem.querySelector("#oauthbtn");

        this.$loginbtn.addEventListener("click", async (event) => {
            event.preventDefault();
            loginAPI.sendData = {
                email: this.$form.querySelector("#email").value,
                password: this.$form.querySelector("#password").value,
            };
            try {
                await loginAPI.request();
                info.myID = loginAPI.recvData.data.user.id;
                info.myUsername = loginAPI.recvData.data.user.username;
                this.requestShift("main_page");
            }
            catch (e) {
                // location.href = location.origin + location.pathname;
                location.reload();
                alert(`Login: ${e.message}`);
            }
        });

        this.$signupbtn.addEventListener("click", () => {
            this.requestShift("signup_subpage");
        });

        // oauth -> should be modified
        // now always 
        this.$oauthbtn.addEventListener("click", () => {
            window.location.href = "http://localhost:8000/oauth/login";
            this.parent.parent.init(); // may be removed later
            this.parent.parent.checkLoggedIn(); // may be removed later
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