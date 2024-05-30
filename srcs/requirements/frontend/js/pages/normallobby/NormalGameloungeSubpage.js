import SubPage from "../SubPage.js";
import { info } from "../../models/Info.js";

class NormalGameloungeSubpage extends SubPage {
    sock;
    $canvas;
    context;

    skeletonRender() {
        this.$elem.innerHTML = `
            <canvas width="1024" height="1024"></canvas>
        `;

        this.$canvas = this.$elem.querySelector("canvas");
        this.context = this.$canvas.getContext("2d");

        
    }

    init() {

    }

    fini() {

    }
};