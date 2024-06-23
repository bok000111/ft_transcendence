import { rootPage } from "../pages/RootPage.js";
import { info, MODE } from "./Info.js";

export class GameSocket {
    ws;
    handler = {
        wait: (data) => {},
        start: (data) => {},
        game: (data) => {},
        end: (data) => {},
        error: (data) => {},
    };
    url;

    constructor() {
        this.ws = null;
        this.url = "ws://localhost:8000/ws/";
    }

    setup() {
        this.ws = new WebSocket(this.url);
        this.ws.addEventListener("open", () => {
            this.ws.addEventListener("message", ({ data }) => {
                const obj = JSON.parse(data);
    
                this.handler[obj.action](obj.data);
            });
            if (info.games.type === MODE.LOCAL) {
                this.send(JSON.stringify({
                    action: "join",
                    data: {
                        type: info.games.type,
                        nickname: "player1",
                    },
                }));
                this.send(JSON.stringify({
                    action: "join",
                    data: {
                        type: info.games.type,
                        nickname: "player2",
                    },
                }));
            }
            else {
                this.send(JSON.stringify({
                    action: "join",
                    data: {
                        type: info.games.type,
                        nickname: document.querySelector("#nickname").value,
                    },
                }));
            }
        });
        this.ws.addEventListener("close", () => {
            this.ws = null;
            this.unmount("wait");
            this.unmount("start");
            this.unmount("game");
            this.unmount("close");
            this.unmount("error");
            rootPage.curChild.curChild.route("main_page/main_subpage");
        });
        // error event 처리는 어떻게 할 것인가?
    }

    close() {
        if (this.ws !== null) {
            this.ws.close();
        }
    }

    isOpen() {
        return this.ws !== null;
    }

    send(msg) {
        this.ws.send(msg);
    }

    mount(action, handler) {
        this.handler[action] = handler;
    }

    unmount(action) {
        this.handler[action] = (data) => {};
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