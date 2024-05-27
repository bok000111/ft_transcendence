import SubPage from "../SubPage.js";
import { normalLobbyAPI } from "../../models/API.js";
import { info } from "../../models/Info.js";

class NormalLobbySubpage extends SubPage {
    $title;
    $players;
    $exitBtn;
    $readyBtn;
    $startBtn;

    render({ data }) {
        this.$players.innerHTML = ``;

        for (player of data.lobby.players) {
            const newNode = document.createElement("li");

            newNode.innerHTML = `
                <div id="${player.nickname}">
                    <h3>${player.nickname}</h3>
                </div>
            `;
            this.$players.appendChild(newNode);
        }
    }

    async refresh() {
        try {
            await normalLobbyAPI.request();
            this.render(normalLobbyAPI.recvData);
        }
        catch (e) {
            alert(`Normal Lobby: ${e.message}`);
        }
    }

    init() {
        try {
            this.sock = new WebSocket(`ws://localhost:8000/ws/lobby/${info.lobby.id}/`);
        }
        catch (e) {
            alert(`Normal Lobby: ${e.message}`);
            this.requestShift("normal_list");
        }

        this.$elem.innerHTML = `
            <h2></h2>
            <ol></ol>
            ${info.lobby.is_host ? `<button id="normal-start">시작</button>` : `<button id="normal-ready">준비</button>`}
            <button id="normal-exit">나가기</button>
        `;

        this.$title = this.$elem.querySelector("h2");
        this.$players = this.$elem.querySelector("ol");
        this.$readyBtn = this.$elem.querySelector("#normal-ready");
        this.$startBtn = this.$elem.querySelector("#normal-start");
        this.$exitBtn = this.$elem.querySelector("#normal-exit");

        this.$exitBtn.addEventListener("click", () => {
            this.requestShift("normal_list_subpage");
        });
    }

    fini() {
        if (this.sock) {
            this.sock.close();
            this.sock = null;
        }
        this.$elem.innerHTML = ``;
    }
};