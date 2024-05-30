import SubPage from "../SubPage.js";
import { tourMakeAPI } from "../../models/API.js";
import { info } from "../../models/Info.js";
import { tourLobbyPage } from "./TourLobbyPage.js";

class TourMakeSubpage extends SubPage {
    $form;
    $backBtn;

    init() {
        this.$elem.innerHTML = `
            <h2>로비 생성</h2>
            <form>
                <input id="lobby-name" type="text" placeholder="lobby-name">
                <input id="nickname" type="text" placeholder="nickname">
                <input type="submit" value="생성"
            </form>
            <button>뒤로 가기</button>
        `;

        this.$form = this.$elem.querySelector("form");
        this.$backBtn = this.$elem.querySelector("button");

        this.$form.addEventListener("submit", async (event) => {
            event.preventDefault();
            tourMakeAPI.sendData.name = this.$form.querySelector("#lobby-name").value;
            tourMakeAPI.sendData.nickname = this.$form.querySelector("#nickname").value;
            try {
                await tourMakeAPI.request();
                info.lobby.id = tourMakeAPI.recvData.data.lobby.id;
                info.lobby.nickname = tourMakeAPI.sendData.nickname;
                info.lobby.players = structuredClone(tourMakeAPI.recvData.data.lobby.players);
                this.requestShift("tour_lobby_subpage");
            }
            catch (e) {
                alert(`Tournament Make Room: ${e.message}`);
                this.$form.querySelector("#lobby-name").value = "";
                this.$form.querySelector("#nickname").value = "";
            }
        });

        this.$backBtn.addEventListener("click", () => {
            this.requestShift("tour_list_subpage");
        });
    }

    fini() {
        this.$elem.innerHTML = ``;
    }
};

export const tourMakeSubpage = new TourMakeSubpage(
    tourLobbyPage.$elem.querySelector("div"),
    tourLobbyPage,
    null,
    "tour_make_subpage"
);