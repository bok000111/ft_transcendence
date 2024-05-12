import { RootPage, rootPage } from "./RootPage.js";

export default class Page extends RootPage {
    requestShift(nextChild) {
        this.parent.childShift(nextChild);
    }

    childShift(nextChild) {
        this.curChild.fini();
        this.curChild = this.child[nextChild];
        this.curChild.init();
    }

    fini() {
        this.childShift(initChildName);
    }
};