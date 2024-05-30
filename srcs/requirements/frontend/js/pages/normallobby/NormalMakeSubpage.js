import SubPage from "../SubPage.js";
import { normalMakeAPI } from "../../models/API.js";
import { info } from "../../models/Info.js";

class NormalMakeSubpage extends SubPage {
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
            normalMakeAPI.sendData.name = this.$form.querySelector("#lobby-name").value;
            normalMakeAPI.sendData.nickname = this.$form.querySelector("#nickname").value;
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