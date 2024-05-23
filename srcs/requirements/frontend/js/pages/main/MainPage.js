import { rootPage } from "../RootPage.js"
import Page from "../Page.js"
import { logoutAPI } from "../../models/API.js"
import { mainSubpage } from "./MainSubpage.js"

// 추가로 다른 "페이지" 추가해야함. (for shift)

class MainPage extends Page {
    $logoutBtn;
    $participateBtn;
    $tournamentResultBtn;
    $matchmakingBtn;

    init() {
        this.$elem.classList.remove("none");
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

    setEvent() {}
}

export const mainPage = new MainPage(
    rootPage.$elem.querySelector(".main-page"),
    rootPage,
    "main_subpage",
    "main_page",
);