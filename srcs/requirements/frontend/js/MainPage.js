import Page from "./Page.js";
import Component from "./Component.js";

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
            this.shift("tourn_result_page");
        });
        this.$matchmakingBtn.addEventListener("click", () => {
            this.shift("match_making_page");
        });
    }
}
