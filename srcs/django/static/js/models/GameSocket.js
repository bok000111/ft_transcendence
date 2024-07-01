import { rootPage } from "../pages/RootPage.js";
import { gamePage } from "../pages/game/GamePage.js";
import { info } from "./Info.js";
import { BASE_WS_URL } from "./API.js";

const STATE = {
    CONNECTING: 0,
    OPEN: 1,
    CLOSING: 2,
    CLOSED: 3,
}

export class GameSocket {
    ws;
    handler = {
        wait: (data) => { },
        start: (data) => { },
        game: (data) => { },
        end: (data) => { },
    };
    url;

    constructor() {
        this.ws = null;
        this.url = BASE_WS_URL;
    }

    setup() {
        this.ws = new WebSocket(this.url, ['jwt.access_token', 'jwt.access_token.' + window.localStorage.getItem("access_token")]);
        this.ws.addEventListener("open", () => {
            this.ws.addEventListener("message", ({ data }) => {
                const obj = JSON.parse(data);
                console.log(obj);

                this.handler[obj.action](obj.data);
            });
            this.send(JSON.stringify({
                action: "join",
                data: {
                    type: info.games.type,
                    nickname: document.querySelector("#nickname").value,
                },
            }));
            document.querySelector("#nickname").value = "";
        });
        this.ws.addEventListener("close", () => {
            this.ws = null;
            this.unmount("wait");
            this.unmount("start");
            this.unmount("game");
            this.unmount("close");
            rootPage.curChild.curChild.route("main_page/main_subpage");
            gamePage.curChild = gamePage.child["pong_subpage"];
        });
        // error event 처리는 어떻게 할 것인가?
    }

    close() {
        if (this.ws !== null) {
            this.ws.close();
        }
    }

    isOpen() {
        return (this.ws !== null && this.ws.readyState === STATE.OPEN);
    }

    send(msg) {
        this.ws.send(msg);
    }

    mount(action, handler) {
        this.handler[action] = handler;
    }

    unmount(action) {
        this.handler[action] = (data) => { };
    }
};

export const gameSocket = new GameSocket();

window.addEventListener("beforeunload", () => {
    if (gameSocket.isOpen()) {
        gameSocket.send(JSON.stringify({
            action: "leave",
            data: null,
        }));
        gameSocket.close();
    }
});