import RootPage from "./RootPage.js";

export default class Page extends RootPage {
    requestShift(nextChildName) {
        this.parent.childShift(nextChildName);
    }

    childShift(nextChildName) {
        this.curChild.fini();
        if (this.selfName === nextChildName) {
            this.requestShift(nextChildName);
        }
        else {
            this.curChild = this.child[nextChildName];
            this.curChild.init();
        }
    }

    init() {
        this.curChild.init();
        this.$elem.classList.remove("none");
    }

    fini() {
        this.$elem.classList.add("none");
        this.curChild = this.child[this.initChildName];
    }
};