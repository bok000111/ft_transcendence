import { rootPage } from "../RootPage.js"
import Page from "../Page.js"

export const tourResultPage = new Page(
    rootPage.$elem.querySelector(".tour-result-page"),
    rootPage,
    "tour_result_list_subpage",
    "tour_result_page"
);