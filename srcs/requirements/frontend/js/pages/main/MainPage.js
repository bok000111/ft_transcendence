import Page from "../Page.js";
import { PageShifter, page_shifter } from "../../shifters/PageShifter.js"
import { main_shifter } from "../../shifters/SubpageShifter.js";

class MainPage extends Page {
    $logoutBtn;
    $participateBtn;
    $tournamentResultBtn;
    $matchmakingBtn;

    setup() {
        this.mount("main_page");
        this.$logoutBtn = this.$elem.querySelector("#logout");
        this.$participateBtn = this.$elem.querySelector("#participate");
        this.$tournamentResultBtn = this.$elem.querySelector("#tournamentResult");
        this.$matchmakingBtn = this.$elem.querySelector("#matchmaking");
    }

    setEvent() {
        this.$logoutBtn.addEventListener("click", () => {
            this.shift("login_page");
        });
        this.$participateBtn.addEventListener("click", () => {
            this.shift("tour_room_page");
        });
        this.$tournamentResultBtn.addEventListener("click", () => {
            this.shift("tour_result_page");
        });
        this.$matchmakingBtn.addEventListener("click", () => {
            this.shift("match_making_page");
        });
    }
}

let mainPage = new MainPage(page_shifter, "main_page");

mainPage = new MainPage(main_shifter, "main_sub_page");