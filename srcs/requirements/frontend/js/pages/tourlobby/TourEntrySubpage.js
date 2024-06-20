import SubPage from "../SubPage.js";
import { tourEntryAPI } from "../../models/API.js";
import { info } from "../../models/Info.js";
import { tourLobbyPage } from "./TourLobbyPage.js";

class TourEntrySubpage extends SubPage {
    $form;
    $backBtn;

    init() {
        this.$elem.innerHTML = `
            <h2>닉네임 입력</h2>
            <form>
                <input id="nickname" type="text" placeholder="nickname">
                <input type="submit" value="입력">
            </form>
            <button>뒤로 가기</button>
        `;

        this.$form = this.$elem.querySelector("form");
        this.$backBtn = this.$elem.querySelector("button");

        this.$form.addEventListener("submit", async (event) => {
            event.preventDefault();
            tourEntryAPI.sendData.nickname = this.$form.querySelector("#nickname").value;
            try {
                await tourEntryAPI.request();
                info.lobby.nickname = tourEntryAPI.sendData.nickname;
                info.lobby.players = structuredClone(tourEntryAPI.recvData.data.lobby.players);
                this.route("tour_lobby_page/tour_lobby_subpage");
            }
            catch (e) {
                alert(`Tournament Entry: ${e.message}`);
                this.$form.querySelector("#nickname").value = "";
            }
        });

        this.$backBtn.addEventListener("click", () => {
            this.route("tour_lobby_page/tour_list_subpage");
        });
    }

    fini() {
        this.$elem.innerHTML = ``;
    }
};

export const tourEntrySubpage = new TourEntrySubpage(
    tourLobbyPage.$elem.querySelector("div"),
    tourLobbyPage,
    null,
    "tour_entry_subpage"
);