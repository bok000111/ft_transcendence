import { mainPage } from "./MainPage.js"
import { logoutAPI } from "../../models/API.js"
import { gameSocket } from "../../models/GameSocket.js";
import { info, MODE } from "../../models/Info.js";
import { rootPage } from "../RootPage.js";
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

    nicknameModalCloseHandler = () => {
        if (this.$nicknameModal.classList.contains("show")) {
            this.nicknameModal.hide();
        }
        gameSocket.close();
    };

    nicknameModalSubmitHandler = (event) => {
        event.preventDefault();
        if (this.$nickname.value === "???") {
            alert("Invalid Nickname...");
            return;
        }
        if (gameSocket.isOpen()) {
            gameSocket.send(JSON.stringify({
                action: "join",
                data: {
                    type: info.games.type,
                    nickname: this.$nickname.value,
                },
            }));
            return;
        }
        gameSocket.setup();
        // 닉네임이 겹친 경우
        gameSocket.mount("error", (data) => {
            alert("Nickname already exists!");
            this.$nickname.value = "";
        });

        gameSocket.mount("wait", (data) => {
            if (this.$nicknameModal.classList.contains("show")) {
                this.nicknameModal.hide();
            }
            this.$waitingModal.querySelector("#waiting-status").textContent = `(${data.waiting_users}/${info.games.maxPlayers})`;
            if (!this.$waitingModal.classList.contains("show")) {
                this.waitingModal.show();
            }
            gameSocket.unmount("error");
        });

        gameSocket.mount("end", (data) => {
            toastNot.makeAlert(data.winner);
            if (data.type === MODE.SUB_GAME) {
                info.changeState(data.winner[0]);
                rootPage.curChild.curChild.route("game_page/tournament_subpage");
            }
            else {
                gameSocket.unmount("start");
                gameSocket.unmount("end");
                gameSocket.close();
            }
        });

        gameSocket.mount("start", (data) => {
            if (info.games.type !== MODE.SUB_GAME) {
                info.games.myNickname = this.$nickname.value;
                gameSocket.unmount("wait");
                gameSocket.unmount("error");

                this.waitingModal.hide();
            }

            if (info.games.type === MODE.TOURNAMENT) {
                info.initState(data.users);
                this.route("game_page/tournament_subpage");
            }
            else {
                info.curGame = data;
                this.route("game_page/pong_subpage");
            }
        });
    };

    $waitingModal;
    waitingModal;

    init() {
        this.$elem.innerHTML = `
            <div class="container z_highest">
                <div class="row justify-content-center mt-5">
                    <div class="col-md-6 col-lg-4">
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="aiGame" class="btn btn-warning btn-lg w-100">AI MODE</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="localGame" class="btn btn-warning btn-lg w-100">LOCAL MODE</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="normalGame-2" class="btn btn-warning btn-lg w-100">NORMAL MODE - 2</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="normalGame-4" class="btn btn-warning btn-lg w-100">NORMAL MODE - 4</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="tourGame" class="btn btn-warning btn-lg w-100">TOURNAMENT MODE</button>
                            </div>
                        </div>
                        <div class="row mb-4 pt-4 pb-3">
                            <div class="col">
                                <button id="tourResult" class="btn btn-warning btn-lg w-100">TOURNAMENT RESULT</button>
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
        this.nicknameModal = new bootstrap.Modal(this.$nicknameModal, {});
        this.$nickname = this.$nicknameModal.querySelector("#nickname");

        this.$waitingModal = document.querySelector("#waitingModal");
        this.waitingModal = new bootstrap.Modal(this.$waitingModal, {});
        
        if (gameSocket.isOpen()) {
            gameSocket.send(JSON.stringify({
                action: "leave",
                data: null,
            }));
            gameSocket.close();
        }
        
        this.$logoutBtn.addEventListener("click" , async() => {
            logoutAPI.sendData = {};
            try {
                await logoutAPI.request();
                this.route("auth_page/login_subpage");
            }
            catch (e) {
                alert(`Logout: ${e.message}`);
            }
        });
        // this.$aiGameBtn.addEventListener("click", () => {
        //     this.nicknameModal.show();
        //     info.games.type = MODE.AI;
        //     info.games.maxPlayers = 2;
        // });
        this.$localGameBtn.addEventListener("click", () => {
            info.games.type = MODE.LOCAL;
            info.games.maxPlayers = 2;

            gameSocket.setup();
            
            gameSocket.mount("wait", (data) => {
                gameSocket.unmount("wait");
                this.$waitingModal.querySelector("#waiting-status").textContent = `(2/2)`;
                this.waitingModal.show();
            });

            gameSocket.mount("end", (data) => {
                gameSocket.unmount("end");
                gameSocket.close();
            });

            gameSocket.mount("start", (data) => {
                gameSocket.unmount("wait");
                gameSocket.unmount("start");
                
                this.waitingModal.hide();

                info.curGame = data;
                this.route("game_page/pong_subpage");
            });
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