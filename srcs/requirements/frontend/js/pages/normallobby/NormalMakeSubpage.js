import SubPage from "../SubPage.js";
import { normalMakeAPI } from "../../models/API.js";
import { info } from "../../models/Info.js";
import { normalLobbyPage } from "./NormalLobbyPage.js";

class NormalMakeSubpage extends SubPage {
    $form;
    $backBtn;

    init() {
        this.$elem.innerHTML = `
            <h2>로비 생성</h2>
            <form>
                <input id="lobby-name" type="text" placeholder="lobby-name">
                <input id="nickname" type="text" placeholder="nickname">
                <h3>
                    <input id="two-players" type="radio" name="max-num">
                    2p
                    <input id="three-players" type="radio" name="max-num">
                    3p
                    <input id="four-players" type="radio" name="max-num">
                    4p
                </h3>
                <input type="submit" value="생성">
            </form>
            <button>뒤로 가기</button>
        `;

        this.$form = this.$elem.querySelector("form");
        this.$backBtn = this.$elem.querySelector("button");

        this.$form.addEventListener("submit", async (event) => {
            event.preventDefault();
            normalMakeAPI.sendData.name = this.$form.querySelector("#lobby-name").value;
            normalMakeAPI.sendData.nickname = this.$form.querySelector("#nickname").value;
            if (this.$form.querySelector("#two-players").checked) {
                normalMakeAPI.sendData.max_players = 2;
            }
            else if (this.$form.querySelector("#three-players").checked) {
                normalMakeAPI.sendData.max_players = 3;
            }
            else if (this.$form.querySelector("#four-players").checked) {
                normalMakeAPI.sendData.max_players = 4;
            }
            else {
                alert("Please check the number of players.");
                return;
            }
            try {
                await normalMakeAPI.request();
                info.lobby.id = normalMakeAPI.recvData.data.lobby.id;
                info.lobby.nickname = normalMakeAPI.sendData.nickname;
                info.lobby.players = structuredClone(normalMakeAPI.recvData.data.lobby.players);
                this.requestShift("normal_lobby_subpage");
            }
            catch (e) {
                alert(`Normal Make Room: ${e.message}`);
                this.$form.querySelector("#lobby-name").value = "";
                this.$form.querySelector("#nickname").value = "";
            }
        });

        this.$backBtn.addEventListener("click", () => {
            this.requestShift("normal_list_subpage");
        });
    }

    fini() {
        this.$elem.innerHTML = ``;
    }
};

export const normalMakeSubpage = new NormalMakeSubpage(
    normalLobbyPage.$elem.querySelector("div"),
    normalLobbyPage,
    null,
    "normal_make_subpage"
);