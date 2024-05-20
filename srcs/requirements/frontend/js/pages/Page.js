import RootPage from "./RootPage.js";

export default class Page extends RootPage {
    requestShift(nextChildName) {
        this.parent.childShift(nextChildName);
    }

    childShift(nextChildName) {
        if (nextChildName.endsWith("_page")) {
            this.requestShift(nextChildName);
        }
        else {
            this.curChild.fini();
            this.curChild = this.child[nextChildName];
            this.curChild.init();
        }
    }

    init() {
        this.child[initChildName].init();
    }

    fini() {
        this.childShift(initChildName);
    }
};