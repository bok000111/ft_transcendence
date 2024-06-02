import SubPage from "../SubPage.js"
import { tourResultPage } from "./TourResultPage.js"
import { tourResultListAPI } from "../../models/API.js"

class TourResultListSubpage extends SubPage {
    $resList;
    $detailArea;

    init() {
        this.$elem.innerHTML = `
            <h2>토너먼트 결과</h2>
            <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Select Tournament
                </button>
                <div class="dropdown-menu" id="result_list" aria-labelledby="dropdownMenuButton">
                    <a class="dropdown-item">Action</a>
                    <a class="dropdown-item">Another action</a>
                    <a class="dropdown-item">Something else here</a>
                </div>
            </div>
            <div id="detail_area"></div>
        `;

        this.$resList = this.$elem.querySelector("#res_list");
        this.$detailArea = this.$elem.querySelector("#detail_area");

        // async () => {
        //     try {
        //         await tourResultListAPI.request();
        //         for(i = 0; i < tourResultListAPI.recvData.data.results.length; i++)
        //         {
        //             const added_text = `<a class="dropdown-item" id="${tourResultListAPI.recvData.data.results[i].id}">${tourResultListAPI.recvData.data.results[i].date}</a>`;
        //             this.$resList.innerHTML += added_text;
        //         }
        //     }
        //     catch (e) {
        //         alert(`Result List: ${e.message}`);
        //         this.requestShift("main_page");
        //     }
        // }
    }

    /*
    각각의 드롭다운 요소들에 대해서 클릭되었을 때 디테일 영역의 HTML을 변경하도록 하는 함수,
    콜백을 통해 addEventListener에서 클릭 되었을 때 디테일 영역을 변경하도록 함.
    */
    // d/etailRender(result_idx) {
    //     this.$detailArea.innerHTML = ``;
    //     this.$detailArea.innerHTML += tourResultListAPI.data.results[i].player1;
    // }

    fini() {
        this.$elem.innerHTML = ``;
    }
}

export const resultListSubpage = new TourResultListSubpage(
    tourResultPage.$elem.querySelector("div"),
    tourResultPage,
    null,
    "tour_result_list_subpage",
)