import { mainPage } from "./MainPage.js"
import { logoutAPI, updateAccessToken } from "../../models/API.js"
import { gameSocket } from "../../models/GameSocket.js";
import { info, MODE } from "../../models/Info.js";
import { rootPage } from "../RootPage.js";
import { gamePage } from "../game/GamePage.js"
import { toastNot } from "../../models/Notification.js"
import SubPage from "../SubPage.js"

class MainSubpage extends SubPage {
    $logoutBtn;
    $aiGameBtn;
    $localGameBtn;
    $normalGame_2Btn;
    $normalGame_4Btn;
    $tourGameBtn;
    $tourResultBtn;

    $nicknameModal;
    nicknameModal;
    $nickname;

    $waitingModal;
    waitingModal;

    nicknameModalCloseHandler = () => {
        if (this.$nicknameModal.classList.contains("show")) {
            this.nicknameModal.hide();
        }
        gameSocket.close();
    };

    waitingModalCloseHandler = () => {
        if (this.$waitingModal.classList.contains("show")) {
            this.waitingModal.hide();
        }
        gameSocket.close();
    };

    AILocalHandler = () => {
        gameSocket.setup();

        gameSocket.mount("end", (data) => {
            gameSocket.unmount("end");
            gameSocket.close();
            toastNot.makeAlert(data.winner);
        });

        gameSocket.mount("start", (data) => {
            gameSocket.unmount("start");

            info.curGame = data;
            this.route("game_page/pong_subpage");
        });
    };

    nicknameModalSubmitHandler = (event) => {
        event.preventDefault();
        if (this.$nickname.value === "???" || this.$nickname.value === "") {
            alert("Invalid Nickname...");
            return;
        }
        gameSocket.setup();

        gameSocket.mount("wait", (data) => {
            if (this.$nicknameModal.classList.contains("show")) {
                this.nicknameModal.hide();
            }
            this.$waitingModal.querySelector("#waiting-status").textContent = `(${data.waiting_users}/${info.games.maxPlayers})`;
            if (!this.$waitingModal.classList.contains("show")) {
                this.waitingModal.show();
            }
        });

        gameSocket.mount("end", (data) => {
            toastNot.makeAlert(data.winner);
            if (data.type === MODE.SUB_GAME) {
                info.changeState(data.winner[0]);
                if (info.curGame.id === data.id) {
                    rootPage.curChild.curChild.route("game_page/tournament_subpage");
                }
                else if (rootPage.curChild.curChild.selfName === "tournament_subpage") {
                    rootPage.curChild.curChild.draw();
                }
            }
            else {
                gameSocket.unmount("start");
                gameSocket.unmount("end");
                gameSocket.close();
            }
        });

        gameSocket.mount("start", (data) => {
            if (data.type !== MODE.SUB_GAME) {
                info.games.myNickname = data.my_nickname;
                gameSocket.unmount("wait");

                this.waitingModal.hide();
            }

            if (data.type === MODE.TOURNAMENT) {
                gamePage.curChild = gamePage.child["tournament_subpage"];
                info.initState(data.users);
                this.route("game_page/tournament_subpage");
            }
            else {
                info.curGame = data;
                this.route("game_page/pong_subpage");
            }
        });
    };

    init() {
        this.$elem.innerHTML = `
            <div class="container z_highest">
                <div class="row justify-content-center mt-5">
                    <div class="col-md-6 col-lg-4">
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="aiGame" class="btn btn-light btn-lg w-100">AI MODE</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="localGame" class="btn btn-light btn-lg w-100">LOCAL MODE</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="normalGame-2" class="btn btn-light btn-lg w-100">NORMAL MODE - 2</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="normalGame-4" class="btn btn-light btn-lg w-100">NORMAL MODE - 4</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="tourGame" class="btn btn-light btn-lg w-100">TOURNAMENT MODE</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="tourResult" class="btn btn-light btn-lg w-100">TOURNAMENT RESULT</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="logout" class="btn btn-danger btn-lg w-100">LOGOUT</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.$logoutBtn = document.querySelector("#logout");
        this.$aiGameBtn = this.$elem.querySelector("#aiGame");
        this.$localGameBtn = this.$elem.querySelector("#localGame");
        this.$normalGame_2Btn = this.$elem.querySelector("#normalGame-2");
        this.$normalGame_4Btn = this.$elem.querySelector("#normalGame-4");
        this.$tourGameBtn = this.$elem.querySelector("#tourGame");
        this.$tourResultBtn = this.$elem.querySelector("#tourResult");

        this.$nicknameModal = document.querySelector("#nicknameModal");
        this.nicknameModal = new bootstrap.Modal(this.$nicknameModal, { backdrop: "static", keyboard: false });
        this.$nickname = this.$nicknameModal.querySelector("#nickname");

        this.$waitingModal = document.querySelector("#waitingModal");
        this.waitingModal = new bootstrap.Modal(this.$waitingModal, { backdrop: "static", keyboard: false });

        if (gameSocket.isOpen()) {
            gameSocket.send(JSON.stringify({
                action: "leave",
                data: null,
            }));
            gameSocket.close();
        }
        this.$logoutBtn.addEventListener("click", async () => {
            logoutAPI.sendData = {};
            try {
                await logoutAPI.request();
                updateAccessToken(null);
                this.route("auth_page/login_subpage");
            }
            catch (e) {
                alert(`Logout: ${e.message}`);
            }
        });
        this.$aiGameBtn.addEventListener("click", () => {
            info.games.type = MODE.AI;
            info.games.maxPlayers = 2;
            this.AILocalHandler();
        });
        this.$localGameBtn.addEventListener("click", () => {
            info.games.type = MODE.LOCAL;
            info.games.maxPlayers = 2;
            this.AILocalHandler();
        });
        this.$normalGame_2Btn.addEventListener("click", () => {
            this.nicknameModal.show();
            info.games.type = MODE.NORMAL_2;
            info.games.maxPlayers = 2;
        });
        this.$normalGame_4Btn.addEventListener("click", () => {
            this.nicknameModal.show();
            info.games.type = MODE.NORMAL_4;
            info.games.maxPlayers = 4;
        });
        this.$tourGameBtn.addEventListener("click", () => {
            this.nicknameModal.show();
            info.games.type = MODE.TOURNAMENT;
            info.games.maxPlayers = 4;
        });
        this.$tourResultBtn.addEventListener("click", () => {
            this.route("tour_result_page/tour_result_list_subpage");
        });

        this.$nicknameModal.addEventListener("submit", this.nicknameModalSubmitHandler);
        this.$nicknameModal.querySelector("#closeBtn").addEventListener("click", this.nicknameModalCloseHandler);
        this.$waitingModal.querySelector("#closeBtn").addEventListener("click", this.waitingModalCloseHandler);
    }

    fini() {
        this.$elem.innerHTML = ``;
    }
}

export const mainSubpage = new MainSubpage(
    mainPage.$elem.querySelector("div"),
    mainPage,
    null,
    "main_subpage",
);