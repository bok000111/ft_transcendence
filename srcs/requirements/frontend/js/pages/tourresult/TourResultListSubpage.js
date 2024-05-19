import SubPage from "../SubPage.js"
import { tourResultPage } from "./TourResultPage.js"
import { tourResultListInfo, tourResultDetailInfo } from "../../models/Info.js"

class TourResultListSubpage extends SubPage {
    $dv;

    init() {
        this.$elem.innerHTML = `
            <h2>토너먼트 결과</h2>
            <div id="result_sub_area"></div>
        `;

        this.$dv = $elem.querySelector("#result_sub_area");
        tourResultListInfo.sendData = null;
        async () => {
            try {
                await tourResultListInfo.requestAPI();
                // for(let i = 0; i < tourResultListInfo.recvData.length; i++)
                // {
                //     this.$dv.innerHTML += `
                //     <div>
                //      <button id=${tourResultListInfo.recvData[i].tournamentID}>${tourResultListInfo.recvData[i].date}</button>
                //     </div>
                //     `;
                // }
                this.setEvent();
            }
            catch (e) {
                alert(`Result List: ${e.message}`);
                this.requestShift("main_page");
            }
        }
    }

    fini() {
        this.$elem.innerHTML = ``;
    }

    setEvent() {
        // for (let i = 0; i < tourResultListInfo.recvData.length; i++)
        // {
        //     let temp = this.$dv.querySelector("${tourResultListInfo.recvData[i].tournamentID}");
        //     temp.addEventListener("click", () => {
        //         resultDetailInfo.sendData.tournamentID = tourResultListInfo.recvData[i].tournamentID;
        //         this.requestShift("tour_result_detail_subpage");
        //     });
        // }
    }
}

export const resultListSubpage = new TourResultListSubpage(
    tourResultPage.$elem.querySelector("div"),
    tourResultPage,
    null,
    "tour_result_list_subpage",
)