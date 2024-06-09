import { mainPage } from "./MainPage.js"
import { logoutAPI } from "../../models/API.js"
import SubPage from "../SubPage.js"

class MainSubpage extends SubPage {
    $logoutBtn;
    $aiGameBtn;
    $localGameBtn;
    $normalGame_2Btn;
    $normalGame_4Btn;
    $tourGameBtn;
    $tourResultBtn;
    nicknameModal;

    init() {
        // this.validate();
        this.$elem.innerHTML = `
            <div class="container z_highest">
                <div class="row justify-content-center mt-5">
                    <div class="col-md-6 col-lg-4">
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="aiGame" class="btn btn-warning btn-lg w-100">AI MODE</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="localGame" class="btn btn-warning btn-lg w-100">LOCAL MODE</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="normalGame-2" class="btn btn-warning btn-lg w-100">NORMAL MODE - 2</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="normalGame-4" class="btn btn-warning btn-lg w-100">NORMAL MODE - 4</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="tourGame" class="btn btn-warning btn-lg w-100">TOURNAMENT MODE</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="tourResult" class="btn btn-warning btn-lg w-100">TOURNAMENT RESULT</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="logout" class="btn btn-danger btn-lg w-100">LOGOUT</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.$logoutBtn = document.querySelector("#logout");
        this.$aiGameBtn = this.$elem.querySelector("#aiGame");
        this.$localGameBtn = this.$elem.querySelector("#localGame");
        this.$normalGame_2Btn = this.$elem.querySelector("#normalGame-2");
        this.$normalGame_4Btn = this.$elem.querySelector("#normalGame-4");
        this.$tourGameBtn = this.$elem.querySelector("#tourGame");
        this.$tourResultBtn = this.$elem.querySelector("#tourResult");
        this.nicknameModal = new bootstrap.Modal(document.querySelector("#nicknameModal"), {});
        
        this.$logoutBtn.addEventListener("click" , async() => {
            logoutAPI.sendData = {};
            try {
                await logoutAPI.request();
                this.route("auth_page/login_subpage");
            }
            catch (e) {
                alert(`Logout: ${e.message}`);
            }
        });
        // this.$tourGameBtn.addEventListener("click", () => {
        //     this.route("tour_lobby_page/tour_list_subpage")
        // });
        this.$normalGame_2Btn.addEventListener("click", () => {
            this.nicknameModal.show();
        });
        // this.$localGameBtn.addEventListener("click", () => {
        //     this.route("local_game_page");
        // });
        this.$tourResultBtn.addEventListener("click", () => {
            this.route("tour_result_page/tour_result_list_subpage");
        });
    }

    fini() {
        this.$elem.innerHTML = ``;
    }
}

export const mainSubpage = new MainSubpage(
    mainPage.$elem.querySelector("div"),
    mainPage,
    null,
    "main_subpage",
);