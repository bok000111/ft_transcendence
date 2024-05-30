import { mainPage } from "./MainPage.js"
import SubPage from "../SubPage.js"
import { logoutAPI } from "../../models/API.js"

class MainSubpage extends SubPage {
    $logoutBtn;
    $participateBtn;
    $tournamentResultBtn;
    $normalBtn;

    init() {
        this.$elem.innerHTML = `
        <div class="container z_highest">
            <div class="row justify-content-center mt-5">
                <div class="col-md-6 col-lg-4">
                    <div class="row mb-4 pt-4 pb-3">
                        <div class="col">
                            <button id="participate" class="btn btn-warning btn-lg btn-block">PARTICIPATE TOURNAMENT</button>
                        </div>
                    </div>
                    <div class="row mb-4 pt-4 pb-3">
                        <div class="col">
                            <button id="tournamentResult" class="btn btn-warning btn-lg btn-block">TOURNAMENT RESULT</button>
                        </div>
                    </div>
                    <div class="row mb-4 pt-4 pb-3">
                        <div class="col">
                            <button id="normalgame" class="btn btn-warning btn-lg btn-block">NORMAL GAME</button>
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
        this.$participateBtn = document.querySelector("#participate");
        this.$tournamentResultBtn = document.querySelector("#tournamentResult");
        this.$normalBtn = document.querySelector("#normalgame");

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
        //this.$participateBtn.addEventListener("click", this.requestShift("tour_room_page")); // 나중에 인자 이름 체킹 필요
        //this.$tournamentResultBtn.addEventListener("click", this.requestShift("tour_result_page")); // 나중에 인자 이름 체킹 필요
        //this.$normalBtn.addEventListener("click", this.requestShift("match_making_page")); // 나중에 인자 이름 체킹 필요
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