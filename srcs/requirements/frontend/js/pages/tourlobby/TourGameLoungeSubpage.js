import SubPage from "../SubPage.js";
import { tourLobbyPage } from "./TourLobbyPage.js";

const canvasWidth = 1200;
const canvasHeight = 900;
const gridWidth = canvasWidth / 10;
const gridHeight = canvasHeight / 20;
const rectWidth = gridWidth * 3 / 2;
const rectHeight = gridHeight * 2;

class TourGameLoungeSubpage extends SubPage {
    $canvas;
    ctx;

    drawLine(startX, startY, endX, endY) {
        this.ctx.moveTo(startX * gridWidth, startY * gridHeight);
        this.ctx.lineTo(endX * gridWidth, endY * gridHeight);
    }

    drawRect(centerX, centerY) {
        this.ctx.fillRect(centerX * gridWidth - rectWidth / 2, centerY * gridHeight - rectHeight / 2, rectWidth, rectHeight);
    }

    drawText(centerX, centerY, text) {
        this.ctx.fillText(text, centerX * gridWidth, centerY * gridHeight);
    }

    drawLines(color) {
        this.ctx.beginPath();
        this.ctx.strokeStyle = color;
        this.drawLine(1, 4, 3, 4);
        this.drawLine(1, 16, 3, 16);
        this.drawLine(7, 4, 9, 4);
        this.drawLine(7, 16, 9, 16);
        this.drawLine(3, 4, 3, 16);
        this.drawLine(7, 4, 7, 16);
        this.drawLine(3, 10, 7, 10);
        this.ctx.stroke();
    }

    drawBoxes(color) {
        this.ctx.fillStyle = color;
        this.drawRect(1, 4);
        this.drawRect(1, 16);
        this.drawRect(9, 4);
        this.drawRect(9, 16);
        this.drawRect(3, 10);
        this.drawRect(7, 10);
    }

    drawTexts(color) {
        this.ctx.fillStyle = color;
        this.ctx.strokeStyle = color;
        this.drawText(1, 4, "player1");
        this.drawText(1, 16, "player2");
        this.drawText(9, 4, "player3");
        this.drawText(9, 16, "player4");
        this.drawText(3, 10, "player5");
        this.drawText(7, 10, "player6");
    }

    skeletonRender() {
        /**
         * canvas 열심히 그리기
         * 패배한 경우 빨갛게 처리하기
         * 승리한 경우 냅두기
         */
        const playerBoxWidth = 100;
        const playerBoxHeight = 50;

        this.drawLines("black");
        this.drawBoxes("black");
    }

    detailRender() {
        this.drawTexts("white");
    }

    init() {
        this.$elem.innerHTML = `
            <h2>토너먼트 현황</h2>
            <canvas canvasWidth="${canvasWidth}" canvasHeight="${canvasHeight}"></canvas>
        `;

        this.$canvas = this.$elem.querySelector("canvas");
        this.ctx = this.$canvas.getContext("2d");

        this.ctx.textAlign = "center";
        this.ctx.textBaseline = "middle";
        this.ctx.font = `${rectHeight / 2}px serif`;

        this.skeletonRender();
    }

    fini() {
        this.$elem.innerHTML = ``;
    }
};

export const tourGameLoungeSubpage = new TourGameLoungeSubpage(
    tourLobbyPage.$elem.querySelector("div"),
    tourLobbyPage,
    null,
    "tour_game_lounge_subpage"
);