import Page from "../Page.js"
import { resultDetailInfo } from "../../models/Info.js"

class resultDetail extends Page {
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