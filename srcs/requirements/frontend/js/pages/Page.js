import RootPage from "./RootPage.js";

export default class Page extends RootPage {
    requestShift(nextChildName) {
        this.parent.childShift(nextChildName);
    }

    childShift(nextChildName) {
        const pageName = nextChildName.split("/")[0];
        const subpageName = nextChildName.split("/")[1];
    
        this.curChild.fini();
        if (this.selfName !== pageName) {
            this.requestShift(pageName);
        }
        else {
            this.curChild = this.child[subpageName];
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