import Page from "../Page.js"
import { resultDetailInfo } from "../../models/Info.js"
import { PageShifter } from "../../shifters/PageShifter.js";
import { tour_res_shifter } from "../../shifters/SubpageShifter.js";

class resultDetailPage extends Page {
    $detailList;
    $homeBtn;

    setup() {
        this.homeBtn = document.querySelector("#home");
        this.detailList = document.querySelector("#resultDetail");
    }

    setEvent() {
        this.$homeBtn.addEventListener("click", () => {
            this.shift("main_page");
        });
    }

    init() {
        const detailFromServer = resultDetailInfo();
        //임시 방식. 무조건 수정해야함.
        this.$detailList.innerHTML = `
            ${detailFromServer.map(item => `<li id="tmp">${item}</li>`).join('')}
        `;
    }

    fini() {
        this.detailList.innerHTML = ``;
    }
}

resultDetailPage = TourResultPage(tour_res_shifter, "res_detail_sub_page");