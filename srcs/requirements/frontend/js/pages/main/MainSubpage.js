import { mainPage } from "./MainPage.js"
import SubPage from "../SubPage.js"
import { logoutAPI } from "../../models/API.js"

class MainSubpage extends SubPage {
    $logoutBtn;
    $tourLobbyBtn;
    $tourResultBtn;
    $normalLobbyBtn;
    $localGameBtn;

    init() {
        this.vailidate();
        this.$elem.innerHTML = `
        <div class="container z_highest">
            <div class="row justify-content-center mt-5">
                <div class="col-md-6 col-lg-4">
                    <div class="row mb-4 pt-4 pb-3">
                        <div class="col">
                            <button id="tourLobby" class="btn btn-warning btn-lg btn-block">TOURNAMENT MODE</button>
                        </div>
                    </div>
                    <div class="row mb-4 pt-4 pb-3">
                        <div class="col">
                            <button id="normalLobby" class="btn btn-warning btn-lg btn-block">NORMAL MODE</button>
                        </div>
                    </div>
                    <div class="row mb-4 pt-4 pb-3">
                        <div class="col">
                            <button id="localGame" class="btn btn-warning btn-lg btn-block">LOCAL MODE</button>
                        </div>
                    </div>
                    <div class="row mb-4 pt-4 pb-3">
                        <div class="col">
                            <button id="tourResult" class="btn btn-warning btn-lg btn-block">TOURNAMENT RESULT</button>
                        </div>
                    </div>
                    <div class="row mb-4 pt-4 pb-3">
                        <div class="col">
                            <button id="logout" class="btn btn-danger btn-lg btn-block">LOGOUT</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>`;

        this.$tourLobbyBtn = document.querySelector("#tourLobby");
        this.$normalLobbyBtn = document.querySelector("#normalLobby");
        this.$localGameBtn = this.$elem.querySelector("localGame");
        this.$tourResultBtn = document.querySelector("#tourResult");
        this.$logoutBtn = document.querySelector("#logout");
        
        // this.$tourLobbyBtn.addEventListener("click", () => {
        //     this.route("tour_lobby_page")
        // });
        this.$normalLobbyBtn.addEventListener("click", () => {
            this.route("normal_lobby_page");
        });
        // this.$localGameBtn.addEventListener("click", () => {
        //     this.route("local_game_page");
        // });
        this.$tourResultBtn.addEventListener("click", () => {
            this.route("tour_result_page");
        });
        this.$logoutBtn.addEventListener("click" , async() => {
            logoutAPI.sendData = {};
            try {
                await logoutAPI.request();
                this.route("auth_page");
            }
            catch (e) {
                alert(`Logout: ${e.message}`);
            }
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