import { authPage } from "./AuthPage.js";
import { BASE_WS_URL, loginAPI, jwtAPI, updateAccessToken } from "../../models/API.js";
import { info } from "../../models/Info.js";
import SubPage from "../SubPage.js";

class LoginSubpage extends SubPage {
    $form;
    $oauthbtn;
    $loginbtn;
    $signupbtn;
    $loginModalCloseBtn;
    $loginModal;
    loginModal;
    response;

    loginModalSubmitHandler = async (event) => {
        event.preventDefault();

        try {
            jwtAPI.sendData = {
                code: this.$loginModal.querySelector("input").value,
            };
            await jwtAPI.request();
            this.loginModal.hide();
            updateAccessToken(jwtAPI.recvData.data.access_token);
            this.route("main_page/main_subpage");
        }
        catch {
            alert("Authentication failed..");
        }
    };

    // 인증코드 창 닫는 버튼
    loginModalCloseHandler = () => {
        this.loginModal.hide();
        // 만약 요청보내서 이메일 기껏 날려줬는데 입력 안하고 나가는 상황에서 추가
        // 로 처리해야하는 부분이 있나?
    };

    async init() {
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
                            <div class="mb-3 mt-4 d-flex gap-2">
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
        this.$loginModal = document.querySelector("#loginModal");
        this.loginModal = new bootstrap.Modal(document.querySelector("#loginModal"), { backdrop: "static", keyboard: false });
        this.$loginModalCloseBtn = this.$loginModal.querySelector(".closeBtn");

        this.$loginbtn.addEventListener("click", async (event) => {
            event.preventDefault();
            // 모달 띄우기

            loginAPI.sendData = {
                email: this.$form.querySelector("#email").value,
                password: this.$form.querySelector("#password").value,
            };
            try {
                await loginAPI.request();
                info.myID = loginAPI.recvData.data.user.id;
                info.myUsername = loginAPI.recvData.data.user.username;
                this.$loginModal.addEventListener("submit", this.loginModalSubmitHandler);
                this.loginModal.show();
            }
            catch (e) {
                // location.href = location.origin + location.pathname;
                alert(`Login: ${e.message}`);
                this.loginModal.hide();
            }
        });

        this.$signupbtn.addEventListener("click", () => {
            this.route("auth_page/signup_subpage");
        });

        // oauth -> should be modified
        // now always 
        this.$oauthbtn.addEventListener("click", () => {
            window.location.href = "/oauth/login/";
            this.parent.parent.init(); // may be removed later
            this.parent.parent.checkLoggedIn(); // may be removed later
        });

        this.$loginModalCloseBtn.addEventListener("click", this.loginModalCloseHandler);
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