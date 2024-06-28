import { gamePage } from "./GamePage.js";
import { info } from "../../models/Info.js";
import SubPage from "../SubPage.js";

const WIDTH = 1200;
const HEIGHT = 900;
const GRID_X = WIDTH / 8;
const GRID_Y = HEIGHT / 4;
const RECT_X = GRID_X;
const RECT_Y = GRID_Y * 2 / 3;
const FONT = `${RECT_Y / 2}px serif`;

const pos = [
    { }, // dummy
    { x: 4, y: 1 },
    { x: 2, y: 2 },
    { x: 6, y: 2 },
    { x: 1, y: 3 },
    { x: 3, y: 3 },
    { x: 5, y: 3 },
    { x: 7, y: 3 },
]

class TournamentSubpage extends SubPage {
    $cnvs;
    ctx;

    drawLine(startX, startY, endX, endY) {
        this.ctx.moveTo(GRID_X * startX, GRID_Y * startY);
        this.ctx.lineTo(GRID_X * endX, GRID_Y * endY);
    }

    drawPlayer({ x, y }, { name, lose }) {
        const rectColor = lose ? "gray" : "white";

        this.ctx.fillStyle = rectColor;
        this.ctx.fillRect(GRID_X * x - RECT_X / 2, GRID_Y * y - RECT_Y / 2, RECT_X, RECT_Y);
        this.ctx.fillStyle = "black";
        this.ctx.fillText(name, GRID_X * x, GRID_Y * y);
    }

    draw() {
        this.ctx.fillStyle = "#006AB6";
        this.ctx.fillRect(0, 0, this.$cnvs.width, this.$cnvs.height);

        this.ctx.beginPath();
        this.ctx.strokeStyle = "black";
        this.drawLine(2, 1, 6, 1);
        this.drawLine(2, 1, 2, 2);
        this.drawLine(1, 2, 3, 2);
        this.drawLine(3, 2, 3, 3);
        this.drawLine(1, 2, 1, 3);
        this.drawLine(6, 1, 6, 2);
        this.drawLine(5, 2, 7, 2);
        this.drawLine(7, 2, 7, 3);
        this.drawLine(5, 2, 5, 3);
        this.ctx.stroke();

        this.ctx.font = FONT;
        this.ctx.textAlign = "center";
        this.ctx.textBaseline = "middle";
        for (let i = 1; i < 8; ++i) {
            this.drawPlayer(pos[i], info.games.state[i]);
        }
    }

    init() {
        this.$elem.innerHTML = `
            <h3 id="tournament-title">TOURNAMENT</h3>
            <canvas id="tour-canvas" width="${WIDTH}" height="${HEIGHT}"></canvas>
        `;

        this.$cnvs = this.$elem.querySelector("#tour-canvas");
        this.ctx = this.$cnvs.getContext("2d");

        document.querySelector(".co_line5").classList.add("none");
        document.querySelector(".co_ball1").classList.add("none");
        document.querySelector(".co_ball2").classList.add("none");
        document.querySelector(".co_ball3").classList.add("none");

        this.draw();
    }

    fini() {
        this.$elem.innerHTML = ``;
        document.querySelector(".co_line5").classList.remove("none");
        document.querySelector(".co_ball1").classList.remove("none");
        document.querySelector(".co_ball2").classList.remove("none");
        document.querySelector(".co_ball3").classList.remove("none");
    }
};

export const tournamentSubpage = new TournamentSubpage(
    gamePage.$elem.querySelector("div"),
    gamePage,
    null,
    "tournament_subpage",
);