import { RootPage, rootPage } from "./RootPage.js";

export default class Page extends RootPage {
    mount(subpageName, initFunc, finiFunc, eventInfo) {
        this.subpage[subpageName] = {
            init: initFunc,
            fini: finiFunc,
        }
        if (subpageName === this.initSubpageName)
            this.curSubpage = this.subpage[subpageName];
    }

    shift(nextSubpage) {
        this.curSubpage.fini();
        this.curSubpage = this.subpage[nextSubpage];
        this.curSubpage.init();
    }
};

export const auth = new Page(
    rootPage.$elem.querySelector(".auth-page"),
    rootPage,
    "login_subpage",
    "auth_page",
    {},
);