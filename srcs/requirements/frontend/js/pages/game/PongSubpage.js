import { gamePage } from "./GamePage.js"
import { info, MODE } from "../../models/Info.js"
import { gameSocket } from "../../models/GameSocket.js"
import { gameSetting, keys1, keys2, keys3 } from "../../models/GameSetting.js";
import Subpage from "../SubPage.js"

class PongSubpage extends Subpage {
    // for UI components setup.
    key_case; // # of GameSetting.js keys
    selfNickname;
    ctx;

    $pongTable;
    $scoreArea;
    $nickListArea;
    $player1Area;
    $player2Area;
    $player3Area;
    $player4Area;

    playerNic = [];
    x = [];
    y = [];
    score = [];
    ballX = 400;
    ballY = 400;

    // for checking which key pressed
    players;
    keys;
    gameInterval;
    scoreInterval;

    init() {
        if (info.curGame.type === MODE.LOCAL) {
            this.playerNic.push("player1");
            this.playerNic.push("player2");
        }
        else {
            this.playerNic.push(""); // player 1
            this.playerNic.push(""); // player 2
            this.playerNic.push(""); // player 3
            this.playerNic.push(""); // player 4
        }
        this.selfNickname = info.games.myNickname;
        this.x.push(gameSetting.STICKWIDTH / 2); // player 1
        this.x.push(gameSetting.GAMEWIDTH - gameSetting.STICKWIDTH / 2); //player 2
        this.x.push(gameSetting.GAMEWIDTH / 2); // player3
        this.x.push(gameSetting.GAMEWIDTH / 2); // player4
        this.y.push(gameSetting.GAMEHEIGHT / 2); // player 1
        this.y.push(gameSetting.GAMEHEIGHT / 2); // player 2
        this.y.push(gameSetting.STICKWIDTH / 2); // player 3
        this.y.push(gameSetting.GAMEHEIGHT - gameSetting.STICKWIDTH / 2); // player 4
        this.score.push(0); // player 1
        this.score.push(0); // player 2
        this.score.push(0); // player 3
        this.score.push(0); // player 4

        this.$elem.innerHTML = `
            <div class="d-flex" id="ingame_area">
                <canvas id="pong_table" width="800" height="800"></canvas>
                <div class="d-grid" id="ingame_info">
                    <div id="pong_score">
                        <div class="row">
                        <div class="col"></div>
                        <div class="col hidden" id="player3_area">${this.playerNic[2]} : ${this.score[2]}</div>
                        <div class="col"></div>
                        </div>
                        <div class="row">
                        <div class="col" id="player1_area">${this.playerNic[0]} : ${this.score[0]}</div>
                        <div class="col">VS</div>
                        <div class="col" id="player2_area">${this.playerNic[1]} : ${this.score[1]}</div>
                        </div>
                        <div class="row">
                        <div class="col"></div>
                        <div class="col hidden" id="player4_area">${this.playerNic[3]} : ${this.score[3]}</div>
                        <div class="col"></div>
                        </div>
                    </div>
                    <div id="pong_player_area">
                    <h2>player list</h2>
                    
                    </div>
                </div>
            </div>
        `;

        this.$pongTable = this.$elem.querySelector("#pong_table");
        this.ctx = this.$pongTable.getContext("2d");
        this.$scoreArea = this.$elem.querySelector("#pong_score");
        this.$nickListArea = this.$elem.querySelector("#pong_player_area");
        this.$player1Area = this.$elem.querySelector("#player1_area");
        this.$player2Area = this.$elem.querySelector("#player2_area");
        this.$player3Area = this.$elem.querySelector("#player3_area");
        this.$player4Area = this.$elem.querySelector("#player4_area");

        this.drawList();
        if (info.games.type === MODE.NORMAL_4) {
            this.$player3Area.classList.remove("hidden");
            this.$player4Area.classList.remove("hidden");
            this.gameInterval = setInterval(this.drawGame4, 10);
            this.scoreInterval = setInterval(this.drawScore4, 10);
        }
        else {
            this.gameInterval = setInterval(this.drawGame2, 10);
            this.scoreInterval = setInterval(this.drawScore2, 10);
        }

        gameSocket.mount("game", (data) => {
            this.ballX = parseInt(data.ball.x);
            this.ballY = parseInt(data.ball.y);
            for (let i = 0; i < data.players.length; i++) {
                this.playerNic[i] = data.players[i].nickname;
                this.score[i] = parseInt(data.players[i].score);
                this.x[i] = parseInt(data.players[i].x);
                this.y[i] = parseInt(data.players[i].y);
            }
        });

        this.sendHandler();
    }

    fini() {
        this.$elem.innerHTML = ``;

        gameSocket.unmount("game");
        clearInterval(this.gameInterval);
        clearInterval(this.scoreInterval);
        document.removeEventListener("keyup", this.handleKeyUp);
        document.removeEventListener("keydown", this.handleKeyDown);
    }

    // case : default
    drawGame2 = () => {
        this.ctx.fillStyle = "white";
        this.ctx.fillRect(0, 0, gameSetting.GAMEWIDTH, gameSetting.GAMEHEIGHT);
        // this.ctx.clearRect(0, 0, gameSetting.GAMEWIDTH, gameSetting.GAMEHEIGHT); // center line
        this.ctx.fillStyle = "black";
        this.ctx.fillRect(gameSetting.GAMEWIDTH / 2, 0, 5, gameSetting.GAMEHEIGHT);

        // racket
        this.ctx.fillRect(this.x[0] - gameSetting.STICKWIDTH / 2, this.y[0] - gameSetting.STICKHEIGHT / 2, gameSetting.STICKWIDTH, gameSetting.STICKHEIGHT); // stick1
        this.ctx.fillRect(this.x[1] - gameSetting.STICKWIDTH / 2, this.y[1] - gameSetting.STICKHEIGHT / 2, gameSetting.STICKWIDTH, gameSetting.STICKHEIGHT); // stick2
        this.drawBall();
    };

    // case : MODE.NORMAL_4
    drawGame4 = () => {
        this.ctx.clearRect(0, 0, gameSetting.GAMEWIDTH, gameSetting.GAMEHEIGHT); // center line
        this.ctx.fillStyle = "black";
        this.ctx.fillRect(gameSetting.GAMEWIDTH / 2, 0, 5, gameSetting.GAMEHEIGHT);

        // racket
        this.ctx.fillRect(this.x[0] - gameSetting.STICKWIDTH / 2, this.y[0] - gameSetting.STICKHEIGHT / 2, gameSetting.STICKWIDTH, gameSetting.STICKHEIGHT); // stick1
        this.ctx.fillRect(this.x[1] - gameSetting.STICKWIDTH / 2, this.y[1] - gameSetting.STICKHEIGHT / 2, gameSetting.STICKWIDTH, gameSetting.STICKHEIGHT); // stick2
        this.ctx.fillRect(this.x[2] - gameSetting.STICKHEIGHT / 2, this.y[2] - gameSetting.STICKWIDTH / 2, gameSetting.STICKHEIGHT, gameSetting.STICKWIDTH); // stick3
        this.ctx.fillRect(this.x[3] - gameSetting.STICKHEIGHT / 2, this.y[3] - gameSetting.STICKWIDTH / 2, gameSetting.STICKHEIGHT, gameSetting.STICKWIDTH); // stick4
        this.drawBall();
    };

    drawBall = () => {
        this.ctx.beginPath();
        this.ctx.strokeStyle = "orange";
        this.ctx.fillStyle = "orange";
        this.ctx.arc(this.ballX, this.ballY, gameSetting.BALLRADIUS, 0, Math.PI * 2);
        this.ctx.fill();
        this.ctx.stroke();
    };

    // case : default
    drawScore2 = () => {
        this.$player1Area.innerHTML = `${this.playerNic[0]} : ${this.score[0]}`;
        this.$player2Area.innerHTML = `${this.playerNic[1]} : ${this.score[1]}`;
    };

    // case : MODE.NORMAL_4
    drawScore4 = () => {
        this.$player1Area.innerHTML = `${this.playerNic[0]} : ${this.score[0]}`;
        this.$player2Area.innerHTML = `${this.playerNic[1]} : ${this.score[1]}`;
        this.$player3Area.innerHTML = `${this.playerNic[2]} : ${this.score[2]}`;
        this.$player4Area.innerHTML = `${this.playerNic[3]} : ${this.score[3]}`;
    };

    drawList() {
        for (let i = 0; i < info.curGame.users.length; i++) {
            let player_list = document.createElement("div");
            player_list.innerHTML = `
                <li>${info.curGame.users[i]}</li>
            `;
            this.$nickListArea.appendChild(player_list);
        }
    }

    // handlers for send event
    sendHandler() {
        if (info.curGame.type === MODE.LOCAL) {
            this.key_case = 2;
            this.keys = JSON.parse(JSON.stringify(keys2));
        }
        else {
            // AI should be added
            if (info.curGame.type === MODE.NORMAL_4 && (this.selfNickname === playerNic[2] || this.selfNickname === playerNic[3])) {
                this.key_case = 3;
                this.keys = JSON.parse(JSON.stringify(keys3));
            }
            else {
                this.key_case = 1;
                this.keys = JSON.parse(JSON.stringify(keys1));
            }
        }
        document.addEventListener("keyup", this.handleKeyUp);
        document.addEventListener("keydown", this.handleKeyDown);
    }

    handleKeyUp = (event) => {
        if (event.repeat) {
            return ;
        }
        if (this.key_case === 1) {
            if (event.key === "ArrowUp") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        message: {
                            action: "game_input",
                            data: {
                                game_id: parseInt(info.curGame.id),
                                nickname: this.selfNickname,
                                keyevent: 8,
                            }
                        }
                    }));
                    
                }
            }
            if (event.key === "ArrowDown") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        message: {
                            action: "game_input",
                            data: {
                                game_id: parseInt(info.curGame.id),
                                nickname: this.selfNickname,
                                keyevent: 7,
                            }
                        }
                    }));
                }
            }
        }
        else if (this.key_case === 2) {
            if (event.key === "w") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        message: {
                            action: "game_input",
                            data: {
                                game_id: parseInt(info.curGame.id),
                                nickname: "player1",
                                keyevent: 8,
                            }
                        }
                    }));
                }
            }
            if (event.key === "s") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        message: {
                            action: "game_input",
                            data: {
                                game_id: parseInt(info.curGame.id),
                                nickname: "player1",
                                keyevent: 7,
                            }
                        }
                    }));
                }
            }
            if (event.key === "ArrowUp") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        message: {
                            action: "game_input",
                            data: {
                                game_id: parseInt(info.curGame.id),
                                nickname: "player2",
                                keyevent: 8,
                            }
                        }
                    }));
                }
            }
            if (event.key === "ArrowDown") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        message: {
                            action: "game_input",
                            data: {
                                game_id: parseInt(info.curGame.id),
                                nickname: "player2",
                                keyevent: 7,
                            }
                        }
                    }));
                }
            }
        }
        else {
            if (event.key === "ArrowRight") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        message: {
                            action: "game_input",
                            data: {
                                game_id: parseInt(info.curGame.id),
                                nickname: this.selfNickname,
                                keyevent: 3,
                            }
                        }
                    }));
                }
            }
            if (event.key === "ArrowLeft") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        message: {
                            action: "game_input",
                            data: {
                                game_id: parseInt(info.curGame.id),
                                nickname: this.selfNickname,
                                keyevent: 4,
                            }
                        }
                    }));
                }
            }
        }
    }

    handleKeyDown = (event) => {
        if (event.repeat) {
            return ;
        }
        if (this.key_case === 1) {
            if (event.key === "ArrowUp") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        message: {
                            action: "game_input",
                            data: {
                                game_id: parseInt(info.curGame.id),
                                nickname: this.selfNickname,
                                keyevent: 6,
                            }
                        }
                    }));
                }
            }
            if (event.key === "ArrowDown") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        message: {
                            action: "game_input",
                            data: {
                                game_id: parseInt(info.curGame.id),
                                nickname: this.selfNickname,
                                keyevent: 5,
                            }
                        }
                    }));
                }
            }
        }
        else if (this.key_case === 2) {
            if (event.key === "w") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        message: {
                            action: "game_input",
                            data: {
                                game_id: parseInt(info.curGame.id),
                                nickname: "player1",
                                keyevent: 6,
                            }
                        }
                    }));
                }
            }
            if (event.key === "s") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        message: {
                            action: "game_input",
                            data: {
                                game_id: parseInt(info.curGame.id),
                                nickname: "player1",
                                keyevent: 5,
                            }
                        }
                    }));
                }
            }
            if (event.key === "ArrowUp") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        message: {
                            action: "game_input",
                            data: {
                                game_id: parseInt(info.curGame.id),
                                nickname: "player2",
                                keyevent: 6,
                            }
                        }
                    }));
                }
            }
            if (event.key === "ArrowDown") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        message: {
                            action: "game_input",
                            data: {
                                game_id: parseInt(info.curGame.id),
                                nickname: "player2",
                                keyevent: 5,
                            }
                        }
                    }));
                }
            }
        }
        else {
            if (event.key === "ArrowRight") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        message: {
                            action: "game_input",
                            data: {
                                game_id: parseInt(info.curGame.id),
                                nickname: this.selfNickname,
                                keyevent: 1,
                            }
                        }
                    }));
                }
            }
            if (event.key === "ArrowLeft") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        message: {
                            action: "game_input",
                            data: {
                                game_id: parseInt(info.curGame.id),
                                nickname: this.selfNickname,
                                keyevent: 2,
                            }
                        }
                    }));
                }
            }
        }
    }
};

export const pongSubpage = new PongSubpage(
    gamePage.$elem.querySelector("div"),
    gamePage,
    null,
    "pong_subpage"
);