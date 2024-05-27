import SubPage from "../SubPage.js";
import { normalDetailAPI, normalLobbyAPI } from "../../models/API.js";
import { info } from "../../models/Info.js";

class NormalLobbySubpage extends SubPage {
    $title;
    $players;
    $exitBtn;
    $readyBtn;
    $startBtn;

    async detailRender() {
        this.$players.innerHTML = ``;
        for (player of normalDetailAPI.recvData.data.lobby.players) {
            const newNode = document.createElement("li");

            newNode.innerHTML = `
                <div id="${player.nickname}">
                    <h3>${player.nickname}</h3>
                    ${() => {
                        if (player.is_host) {
                            return `<h4>방장</h4>`;
                        }
                        else if (player.is_ready) {
                            return `<h4>ready</h4>`;
                        }
                        else {
                            return ``;
                        }
                    }}
                </div>
            `;
            this.$players.appendChild(newNode);
        }
    }
    
    skeletonRender() {
        this.$elem.innerHTML = `
            <h2></h2>
            <ol></ol>
            ${info.lobby.players.find(elem => elem.id === info.myID).is_host
                ? `<button id="normal-start">start</button>`
                : `<button id="normal-ready">ready</button>`}
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
    
    /**
     * socket 수신 메시지 구조
     * {
     *     type: "server_message"
     *     data: {
     *         id: number,
     *         nickname: string,
     *         event: "join" | "leave" | "ready" | "start" | "error",
     *         reason: string?,
     *         data: any,
     *     },
     * }
     * 
     * socket 송신 메시지 구조
     * {
     *     type: "client_message"
     *     data: {
     *         event: "leave" | "ready" | "start",
     *         reason: string?,
     *     },
     * }
     * 
     * socket을 통해 메시지가 들어오면, 내용에 따라 다음과 같은 처리를 해 준다.
     * 
     * < 수신 메시지 처리 >
     * - "join" / "leave" -> 사용자를 추가 / 삭제 렌더링을 해 준다.
     * - "ready" -> 사용자 옆에 ready 표시를 띄워준다.
     * - "start" -> requestShift("normal_gamelounge_subpage") 호출
     * - "error" -> requestShift("normal_list_subpage") 호출
     * 
     * < 송신 메시지 처리 >
     * - "leave" -> 사용자가 로비를 나갈 때 전송
     * - "ready" -> 사용자가 ready 버튼을 누르면 전송
     * - "start" -> 사용자가 start 버튼을 누르면 전송
     * 
     */
    messageHandler(event) {
        const data = JSON.parse(event.data).data;

        switch (data.event) {
        case "leave":
            info.lobby.players = info.lobby.players.filter(elem => data.id !== elem.id);
            break;
        case "ready":
            info.lobby.players.find(elem => data.id === elem.id).is_ready = true;
            break;
        case "join":
            info.lobby.players.push({
                id: data.id,
                nickname: data.nickname,
                score: null, // ?
                is_host: false,
                is_ready: false,
            });
        case "start":
            this.requestShift("normal_gamelounge_subpage");
            return;
        case "error":
            this.requestShift("normal_list_subpage");
            return;
        }
        this.detailRender();
    }

    init() {
        this.skeletonRender();
        try {
            this.sock = new WebSocket(`ws://localhost:8000/ws/lobby/${info.lobby.id}/`);
            this.sock.addEventListener("open", async () => {
                try {
                    await normalLobbyAPI.request();
                    this.detailRender();
                }
                catch (e) {
                    alert(`Normal Lobby: ${e.message}`);
                    this.requestShift("normal_list_subpage");
                }
            });
            this.sock.addEventListener("message", (event) => {
                this.messageHandler(event);
            });
            this.sock.addEventListener("error", () => {
                this.requestShift("normal_list_subpage");
            });
        }
        catch (e) {
            alert(`Normal Lobby: ${e.message}`);
            this.requestShift("normal_list_subpage");
        }
    }

    fini() {
        if (this.sock) {
            this.sock.close();
            this.sock = null;
        }
        this.$elem.innerHTML = ``;
    }
};