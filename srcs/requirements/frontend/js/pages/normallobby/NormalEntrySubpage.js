import SubPage from "../SubPage.js";
import { normalEntryAPI } from "../../models/API.js";
import { info } from "../../models/Info.js";

class NormalEntrySubpage extends SubPage {
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
            normalEntryAPI.sendData.nickname = this.$form.querySelector("#nickname").value;
            try {
                await normalEntryAPI.request();
                info.lobby.nickname = normalEntryAPI.sendData.nickname;
                info.lobby.players = structuredClone(normalEntryAPI.recvData.data.lobby.players);
                this.requestShift("normal_lobby_subpage");
            }
            catch (e) {
                alert(`normalnament Entry: ${e.message}`);
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