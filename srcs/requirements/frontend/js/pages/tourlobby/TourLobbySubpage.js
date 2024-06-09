import SubPage from "../SubPage.js";
import { tourDetailAPI, tourLobbyAPI } from "../../models/API.js";
import { info } from "../../models/Info.js";
import { tourLobbyPage } from "./TourLobbyPage.js";

/**
 * TourLobbySubpage -> TourGameLoungeSubpage
 * 이렇게 shift할 경우에는 소켓이 살아 있어야 한다.
 * 나머지 shift의 경우에는 소켓.close() 해 주어야 함.
 * 
 * 1. TourLobbySubpage와 TourGameLoungeSubpage 에다가 sock 변수를 각각 만든다
 *    -> 너무 별로인듯..
 * 2. TourLobbyPage에다가 sock 변수를 만든다.
 *    - TourLobbySubpage <---> TourGameLoungeSubpage 간의 shift -> sock 유지
 *    - 나머지 shift -> sock.close();
 */

class TourLobbySubpage extends SubPage {
    $title;
    $players;
    $exitBtn;
    $readyBtn;
    $startBtn;

    requestShift(nextChildName) {
        if (nextChildName !== "tour_game_lounge_subpage"
            && this.sock !== null) {
            this.sock.close();
        }
        this.parent.childShift(nextChildName);
    }

    async detailRender() {
        this.$players.innerHTML = ``;
        for (player of tourDetailAPI.recvData.data.lobby.players) {
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
                ? `<button id="tour-start">start</button>`
                : `<button id="tour-ready">ready</button>`}
            <button id="tour-leave">leave</button>
        `;

        this.$title = this.$elem.querySelector("h2");
        this.$players = this.$elem.querySelector("ol");
        this.$readyBtn = this.$elem.querySelector("#tour-ready");
        this.$startBtn = this.$elem.querySelector("#tour-start");
        this.$leaveBtn = this.$elem.querySelector("#tour-leave");

        this.$leaveBtn.addEventListener("click", () => {
            this.route("tour_lobby_page/tour_list_subpage");
        });

        if (this.$readyBtn) {
            this.$readyBtn.addEventListener("click", () => {
                this.sock.send(JSON.stringify({
                    type: "client_message",
                    data: {
                        event: "ready",
                    }
                }));
                this.detailRender();
            });
        }
        else {
            this.$startBtn.addEventListener("click", () => {
                this.sock.send(JSON.stringify({
                    type: "client_message",
                    data: {
                        event: "start",
                    }
                }));
            });
        }
        this.$leaveBtn.addEventListener("click", () => {
            this.sock.send(JSON.stringify({
                type: "client_message",
                data: {
                    event: "leave",
                }
            }));
            this.route("tour_lobby_page/tour_list_subpage");
        });
    }

    messageHandler(event) {
        const data = JSON.parse(event.data).data;

        // 이게 맞는지 모르겠다.
        if (data === null || data === undefined) {
            return;
        }

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
            this.route("tour_lobby_page/tour_game_lounge_subpage");
            return;
        case "error":
            this.route("tour_lobby_page/tour_list_subpage");
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
                    await tourLobbyAPI.request();
                    this.detailRender();
                }
                catch (e) {
                    alert(`Tournament Lobby: ${e.message}`);
                    this.route("tour_lobby_page/tour_list_subpage");
                }
            });
            this.sock.addEventListener("message", (event) => {
                this.messageHandler(event);
            });
            this.sock.addEventListener("error", () => {
                this.route("tour_lobby_page/tour_list_subpage");
            });
        }
        catch (e) {
            alert(`Tournament Lobby: ${e.message}`);
            this.route("tour_lobby_page/tour_list_subpage");
        }
    }

    fini() {
        this.$elem.innerHTML = ``;
    }
};

export const tourLobbySubpage = new TourLobbySubpage(
    tourLobbyPage.$elem.querySelector("div"),
    tourLobbyPage,
    null,
    "tour_lobby_subpage"
);