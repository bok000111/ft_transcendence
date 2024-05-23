import SubPage from "../SubPage.js";
import { tourMakeAPI, tourLobbyAPI } from "../../models/API.js";
import { info } from "../../models/Info.js";

class TourMakeSubpage extends SubPage {
    $form;
    $backBtn;

    init() {
        this.$elem.innerHTML = `
            <h2>방 생성</h2>
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
                info.lobby = {
                    id: tourMakeAPI.recvData.data.lobby.id,
                    nickname: tourMakeAPI.sendData.nickname,
                    isHost: true,
                    isReady: false,
                }
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