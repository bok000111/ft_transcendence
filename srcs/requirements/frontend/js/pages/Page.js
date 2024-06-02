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
            const url = location.origin + location.pathname + '#' + nextChildName;
            history.pushState(null, null, url);
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