import RootPage from "./RootPage.js";

export default class Page extends RootPage {
    requestShift(nextChildName) {
        this.parent.childShift(nextChildName);
    }

    childShift(nextChildName) {
        this.curChild.fini();
        if (nextChildName.endsWith("_page")) {
            this.requestShift(nextChildName);
        }
        else {
            this.curChild = this.child[nextChildName];
            this.curChild.init();
        }
    }

    init() {
        this.$elem.classList.remove("none");
        this.curChild.init();
    }

    fini() {
        this.curChild = this.child[initChildName];
        this.$elem.classList.add("none");
    }
};