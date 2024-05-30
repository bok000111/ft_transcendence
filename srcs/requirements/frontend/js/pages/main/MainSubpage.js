import { mainPage } from "./MainPage.js"
import SubPage from "../SubPage.js"
import { logoutAPI } from "../../models/API.js"

class MainSubpage extends SubPage {
    $logoutBtn;
    $tourLobbyBtn;
    $tourResultBtn;
    $normalLobbyBtn;

    init() {
        this.$elem.innerHTML = `
        <div class="container z_highest">
            <div class="row justify-content-center mt-5">
                <div class="col-md-6 col-lg-4">
                    <div class="row mb-4 pt-4 pb-3">
                        <div class="col">
                            <button id="tourLobby" class="btn btn-warning btn-lg btn-block">PARTICIPATE TOURNAMENT</button>
                        </div>
                    </div>
                    <div class="row mb-4 pt-4 pb-3">
                        <div class="col">
                            <button id="tourResult" class="btn btn-warning btn-lg btn-block">TOURNAMENT RESULT</button>
                        </div>
                    </div>
                    <div class="row mb-4 pt-4 pb-3">
                        <div class="col">
                            <button id="normalLobby" class="btn btn-warning btn-lg btn-block">NORMAL GAME</button>
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

        this.$logoutBtn = document.querySelector("#logout");
        this.$tourLobbyBtn = document.querySelector("#tourLobby");
        this.$tourResultBtn = document.querySelector("#tourResult");
        this.$normalLobbyBtn = document.querySelector("#normalLobby");

        this.$logoutBtn.addEventListener("click" , async() => {
            logoutAPI.sendData = {};
            try {
                await logoutAPI.request();
                this.requestShift("auth_page");
            }
            catch (e) {
                alert(`Logout: ${e.message}`);
            }
        });
        //this.$tourLobbyBtn.addEventListener("click", this.requestShift("tour_lobby_page"));
        this.$tourResultBtn.addEventListener("click", () => {
            this.requestShift("tour_result_page");
        });
        this.$normalLobbyBtn.addEventListener("click", () => {
            this.requestShift("normal_lobby_page");
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