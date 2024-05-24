import { mainPage } from "./MainPage.js"
import SubPage from "../SubPage.js"
import { logoutAPI } from "../../models/API.js"

class MainSubpage extends SubPage {
    $logoutBtn;
    $participateBtn;
    $tournamentResultBtn;
    $matchmakingBtn;

    init() {
        this.$elem.innerHTML = `
        <div>
        <button id="logout">Logout</button>
        </div>
        <div>
        <button id="participate">Participate Tournament</button>
        </div>
        <div>
        <button id="tournamentResult">Tournament Result</button>
        </div>
        <div>
        <button id="matchmaking">Matchmaking</button>
        </div>`;

        this.$logoutBtn = document.querySelector("#logout");
        this.$participateBtn = document.querySelector("#participate");
        this.$tournamentResultBtn = document.querySelector("#tournamentResult");
        this.$matchmakingBtn = document.querySelector("#matchmaking");

        this.$logoutBtn.addEventListener("click" , async() => {
            logoutAPI.sendData = {};
            try {
                //await logoutAPI.request();
                this.requestShift("auth_page");
            }
            catch (e) {
                alert(`Logout: ${e.message}`);
            }
        });
        //this.$participateBtn.addEventListener("click", this.requestShift("tour_room_page")); // 나중에 인자 이름 체킹 필요
        //this.$tournamentResultBtn.addEventListener("click", this.requestShift("tour_result_page")); // 나중에 인자 이름 체킹 필요
        //this.$matchmakingBtn.addEventListener("click", this.requestShift("match_making_page")); // 나중에 인자 이름 체킹 필요
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