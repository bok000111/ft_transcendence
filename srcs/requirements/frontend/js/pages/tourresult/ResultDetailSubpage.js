import SubPage from "../SubPage.js"
import { tourResultPage } from "./TourResultPage.js"

class ResultDetailSubpage extends SubPage {
    init() {
        
    }

    fini() {

    }
}

export const resultDetailSubpage = new ResultDetailSubpage(
    tourResultPage.$elem.querySelector("div"),
    tourResultPage,
    null,
    "result_detail_subpage",
);