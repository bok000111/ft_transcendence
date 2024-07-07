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
    $commonBg;
    $Bgelem;
    $line2;
    $line3;
    $line5;
    $ball1;
    $ball2;
    $ball3;

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
            this.playerNic.push("player_1");
            this.playerNic.push("player_2");
        }
        else if (info.curGame.type === MODE.AI) {
            this.playerNic.push("player");
            this.playerNic.push("mingkang bot");
        }
        else {
            this.playerNic.push(""); // player 1
            this.playerNic.push(""); // player 2
            this.playerNic.push(""); // player 3
            this.playerNic.push(""); // player 4
        }
        this.selfNickname = info.games.myNickname;
        if (info.curGame.type === MODE.AI) {
            this.selfNickname = "player";
        }
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
                <div class="d-grid ms-3" id="ingame_info">
                    <div id="pong_score" class="card p-3 mb-3">
                        <div class="card-body">
                            <div class="row mb-3">
                                <div class="col"></div>
                                <div class="col text-center hidden score-cell d-flex flex-column" id="player3_area">
                                    <div class="nickname">${this.playerNic[2]}</div>
                                    <div class="score">${this.score[2]}</div>
                                </div>
                                <div class="col"></div>
                            </div>
                            <div class="row mb-3">
                                <div class="col text-center score-cell d-flex flex-column" id="player1_area">
                                    <div class="nickname">${this.playerNic[0]}</div>
                                    <div class="score">${this.score[0]}</div>
                                </div>
                                <div class="col text-center vs-cell">VS</div>
                                <div class="col text-center score-cell d-flex flex-column" id="player2_area">
                                    <div class="nickname">${this.playerNic[1]}</div>
                                    <div class="score">${this.score[1]}</div>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col"></div>
                                <div class="col text-center score-cell hidden d-flex flex-column" id="player4_area">
                                    <div class="nickname">${this.playerNic[3]}</div>
                                    <div class="score">${this.score[3]}</div>
                                </div>
                                <div class="col"></div>
                            </div>
                        </div>
                    </div>
                    <div id="pong_player_area" class="mt-5">
                        <h2 class="text-center">Player List</h2>
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
        this.$commonBg = document.querySelector(".co_main");
        this.$commonBg.classList.remove("co_main");
        this.$commonBg.classList.remove("co_frame");
        this.$commonBg.classList.add("game_bg");
        this.$Bgelem = document.querySelector(".right-triangle");
        this.$Bgelem.classList.remove("none");

        this.$line2 = document.querySelector(".co_line2");
        this.$line2.classList.add("none");
        this.$line3 = document.querySelector(".co_line3");
        this.$line3.classList.add("none");
        this.$line5 = document.querySelector(".co_line5");
        this.$line5.classList.add("none");
        this.$ball1 = document.querySelector(".co_ball1");
        this.$ball1.classList.add("none");
        this.$ball2 = document.querySelector(".co_ball2");
        this.$ball2.classList.add("none");
        this.$ball3 = document.querySelector(".co_ball3");
        this.$ball3.classList.add("none");

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
        this.$line2.classList.remove("none");
        this.$line3.classList.remove("none");
        this.$line5.classList.remove("none");
        this.$ball1.classList.remove("none");
        this.$ball2.classList.remove("none");
        this.$ball3.classList.remove("none");
        this.$commonBg.classList.add("co_frame");
        this.$commonBg.classList.add("co_main");
        this.$commonBg.classList.remove("game_bg");
        this.$Bgelem.classList.add("none");
    }

    // case : default
    drawGame2 = () => {
        this.ctx.fillStyle = "#006AB6";
        this.ctx.fillRect(0, 0, gameSetting.GAMEWIDTH, gameSetting.GAMEHEIGHT);
        // this.ctx.clearRect(0, 0, gameSetting.GAMEWIDTH, gameSetting.GAMEHEIGHT); // center line
        this.ctx.fillStyle = "white";
        this.ctx.fillRect(gameSetting.GAMEWIDTH / 2 - 2, 0, 5, gameSetting.GAMEHEIGHT);
        this.ctx.fillRect(0, gameSetting.GAMEHEIGHT / 2 - 2, gameSetting.GAMEWIDTH, 5);
        this.ctx.fillRect(0, 718, gameSetting.GAMEWIDTH, 5);
        this.ctx.fillRect(0, 78, gameSetting.GAMEWIDTH, 5);

        // racket
        this.ctx.fillRect(this.x[0] - gameSetting.STICKWIDTH / 2, this.y[0] - gameSetting.STICKHEIGHT / 2, gameSetting.STICKWIDTH, gameSetting.STICKHEIGHT); // stick1
        this.ctx.fillRect(this.x[1] - gameSetting.STICKWIDTH / 2, this.y[1] - gameSetting.STICKHEIGHT / 2, gameSetting.STICKWIDTH, gameSetting.STICKHEIGHT); // stick2
        this.drawBall();
    };

    // case : MODE.NORMAL_4
    drawGame4 = () => {
        this.ctx.fillStyle = "#006AB6";
        this.ctx.fillRect(0, 0, gameSetting.GAMEWIDTH, gameSetting.GAMEHEIGHT);
        this.ctx.fillStyle = "white";
        this.ctx.fillRect(gameSetting.GAMEWIDTH / 2 - 2, 0, 5, gameSetting.GAMEHEIGHT);
        this.ctx.fillRect(0, gameSetting.GAMEHEIGHT / 2 - 2, gameSetting.GAMEWIDTH, 5);
        this.ctx.fillRect(0, 718, gameSetting.GAMEWIDTH, 5);
        this.ctx.fillRect(0, 78, gameSetting.GAMEWIDTH, 5);

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
        this.$player1Area.innerHTML = `
            <div class="nickname">${this.playerNic[0]}</div>
            <div class="score">${this.score[0]}</div>
        `;
        this.$player2Area.innerHTML = `
            <div class="nickname">${this.playerNic[1]}</div>
            <div class="score">${this.score[1]}</div>
        `;
    };

    // case : MODE.NORMAL_4
    drawScore4 = () => {
        this.$player1Area.innerHTML = `
        <div class="nickname">${this.playerNic[0]}</div>
        <div class="score">${this.score[0]}</div>
        `;
        this.$player2Area.innerHTML = `
            <div class="nickname">${this.playerNic[1]}</div>
            <div class="score">${this.score[1]}</div>
        `;
        this.$player3Area.innerHTML = `
            <div class="nickname">${this.playerNic[2]}</div>
            <div class="score">${this.score[2]}</div>
        `;
        this.$player4Area.innerHTML = `
            <div class="nickname">${this.playerNic[3]}</div>
            <div class="score">${this.score[3]}</div>
        `;
    };

    drawList() {
        for (let i = 0; i < info.curGame.users.length; i++) {
            let player_list = document.createElement("div");
            if (info.curGame.type !== MODE.LOCAL && info.curGame.users[i] === this.selfNickname)
            {
                player_list.innerHTML = `
                    <li class="list-group-item d-flex justify-content-between align-items-center">${info.curGame.users[i]}(me)</li>
                `;
            }
            else {
                player_list.innerHTML = `
                    <li class="list-group-item d-flex justify-content-between align-items-center">${info.curGame.users[i]}</li>
                `;
            }
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
            if (info.curGame.type === MODE.NORMAL_4 && (this.selfNickname === info.curGame.users[2] || this.selfNickname === info.curGame.users[3])) {
                this.key_case = 3;
                this.keys = JSON.parse(JSON.stringify(keys3));
            }
            else if (info.curGame.type === MODE.NORMAL_4 && (this.selfNickname === info.curGame.users[0] || this.selfNickname === info.curGame.users[1])) {
                this.key_case = 1;
                this.keys = JSON.parse(JSON.stringify(keys1));
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
        event.preventDefault();
        if (event.repeat) {
            return ;
        }
        if (this.key_case === 1) {
            if (event.key === "ArrowUp") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        action: "game_input",
                        data: {
                            game_id: parseInt(info.curGame.id),
                            nickname: this.selfNickname,
                            keyevent: 8,
                        }
                    }));
                    
                }
            }
            if (event.key === "ArrowDown") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        action: "game_input",
                        data: {
                            game_id: parseInt(info.curGame.id),
                            nickname: this.selfNickname,
                            keyevent: 7,
                        }
                    }));
                }
            }
        }
        else if (this.key_case === 2) {
            if (event.key === "w") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        action: "game_input",
                        data: {
                            game_id: parseInt(info.curGame.id),
                            nickname: "player_1",
                            keyevent: 8,
                        }
                    }));
                }
            }
            if (event.key === "s") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        action: "game_input",
                        data: {
                            game_id: parseInt(info.curGame.id),
                            nickname: "player_1",
                            keyevent: 7,
                        }
                    }));
                }
            }
            if (event.key === "ArrowUp") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        action: "game_input",
                        data: {
                            game_id: parseInt(info.curGame.id),
                            nickname: "player_2",
                            keyevent: 8,
                        }
                    }));
                }
            }
            if (event.key === "ArrowDown") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        action: "game_input",
                        data: {
                            game_id: parseInt(info.curGame.id),
                            nickname: "player_2",
                            keyevent: 7,
                        }
                    }));
                }
            }
        }
        else {
            if (event.key === "ArrowRight") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        action: "game_input",
                        data: {
                            game_id: parseInt(info.curGame.id),
                            nickname: this.selfNickname,
                            keyevent: 3,
                        }
                    }));
                }
            }
            if (event.key === "ArrowLeft") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        action: "game_input",
                        data: {
                            game_id: parseInt(info.curGame.id),
                            nickname: this.selfNickname,
                            keyevent: 4,
                        }
                    }));
                }
            }
        }
    }

    handleKeyDown = (event) => {
        event.preventDefault();
        if (event.repeat) {
            return ;
        }
        if (this.key_case === 1) {
            if (event.key === "ArrowUp") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        action: "game_input",
                        data: {
                            game_id: parseInt(info.curGame.id),
                            nickname: this.selfNickname,
                            keyevent: 6,
                        }
                    }));
                }
            }
            if (event.key === "ArrowDown") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        action: "game_input",
                        data: {
                            game_id: parseInt(info.curGame.id),
                            nickname: this.selfNickname,
                            keyevent: 5,
                        }
                    }));
                }
            }
        }
        else if (this.key_case === 2) {
            if (event.key === "w") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        action: "game_input",
                        data: {
                            game_id: parseInt(info.curGame.id),
                            nickname: "player_1",
                            keyevent: 6,
                        }
                    }));
                }
            }
            if (event.key === "s") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        action: "game_input",
                        data: {
                            game_id: parseInt(info.curGame.id),
                            nickname: "player_1",
                            keyevent: 5,
                        }
                    }));
                }
            }
            if (event.key === "ArrowUp") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        action: "game_input",
                        data: {
                            game_id: parseInt(info.curGame.id),
                            nickname: "player_2",
                            keyevent: 6,
                        }
                    }));
                }
            }
            if (event.key === "ArrowDown") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        action: "game_input",
                        data: {
                            game_id: parseInt(info.curGame.id),
                            nickname: "player_2",
                            keyevent: 5,
                        }
                    }));
                }
            }
        }
        else {
            if (event.key === "ArrowRight") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        action: "game_input",
                        data: {
                            game_id: parseInt(info.curGame.id),
                            nickname: this.selfNickname,
                            keyevent: 1,
                        }
                    }));
                }
            }
            if (event.key === "ArrowLeft") {
                if (gameSocket.isOpen()) {
                    gameSocket.send(JSON.stringify({
                        action: "game_input",
                        data: {
                            game_id: parseInt(info.curGame.id),
                            nickname: this.selfNickname,
                            keyevent: 2,
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