import SubPage from "../SubPage.js";
// import { TourGameLoungeAPI } from "../../models/API.js";

class TourGameLoungeSubpage extends SubPage {
    $canvas;

    draw({ data }) {
        /**
         * canvas 열심히 그리기
         * 패배한 경우 빨갛게 처리하기
         * 승리한 경우 냅두기
         */
    }

    init() {
        this.$elem.innerHTML = `
            <h2>토너먼트 현황</h2>
            <canvas></canvas>
        `;

        this.$canvas = this.$elem.querySelector("canvas");

        this.draw(tourGameLoungeAPI.recvData);
    }

    fini() {

    }
};