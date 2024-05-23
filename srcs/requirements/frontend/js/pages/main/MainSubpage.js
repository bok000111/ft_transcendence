import { mainPage } from "./MainPage.js"
import SubPage from "../SubPage.js"

class MainSubpage extends SubPage {
    init() {}
    fini() {}
}

export const mainSubpage = new MainSubpage(
    mainPage.$elem.querySelector("voidmain"),
    mainPage,
    null,
    "signup_subpage"
);