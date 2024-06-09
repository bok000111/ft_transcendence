import { rootPage } from "../RootPage.js"
import Page from "../Page.js"
import { mainSubpage } from "./MainSubpage.js"

// 추가로 다른 "페이지" 추가해야함. (for shift)

export const mainPage = new Page(
    rootPage.$elem.querySelector(".main-page"),
    rootPage,
    "main_subpage",
    "main_page",
);