import { rootPage } from "../RootPage.js"
import Page from "../Page.js"

export default class TourResultPage extends Page {
    $homeBtn;

    constructor(elem, parent, initChildName, selfName) {
        super(elem);
        this.initChildName = initChildName;
        if (parent)
            parent.mount(selfName, this.init.bind(this), this.fini.bind(this));
    }

    setEvent() {
        homeBtn = document.$elem.querySelector("#to-main");
        homeBtn.addEventListener("click", this.requestShift("main_page"));
    }
}

export const tourResultPage = new TourResultPage(
    rootPage.$elem.querySelector(".tour-result-page"),
    rootPage,
    "tour_result_list_subpage",
    "tour_result_page",
)