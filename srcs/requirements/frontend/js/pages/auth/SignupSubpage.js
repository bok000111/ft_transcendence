import { authPage } from "./AuthPage.js";
import { signupAPI } from "../../models/API.js";
import SubPage from "../SubPage.js";

class SignupSubpage extends SubPage {
    $form;
    $signupbtn;
    $loginbtn;

    init() {
        this.$elem.innerHTML = `
            <div class="container z_highest">
                <div class="row justify-content-center mt-5">
                    <form class="col-md-6 col-lg-4">
                        <h3 class="text-center mb-4">Signup</h3>
                        <div class="mb-4">
                            <label for="email" class="form-label">Email</label>
                            <input id="email" type="text" class="form-control" placeholder="Enter your email">
                        </div>
                        <div class="mb-4">
                            <label for="password" class="form-label">Password</label>
                            <input id="password" type="password" class="form-control" placeholder="Enter your password">
                        </div>
                        <div class="mb-4">
                            <label for="username" class="form-label">Username</label>
                            <input id="username" type="text" class="form-control" placeholder="Enter your username">
                        </div>
                        <div class="d-flex justify-content-between">
                            <button type="submit" class="btn btn-primary">Sign Up</button>
                            <button type="button" class="btn btn-secondary" id="loginbtn">Login</button>
                        </div>
                    </form>
                </div>
            </div>
        `;

        this.$form = this.$elem.querySelector("form");
        this.$signupbtn = this.$elem.querySelector("#signupbtn");
        this.$loginbtn = this.$elem.querySelector("#loginbtn");

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
                this.route("login_subpage");
            }
            catch (e) {
                alert(`Signup: ${e.message}`);
            }
        });

        this.$loginbtn.addEventListener("click", () => {
            this.route("login_subpage");
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