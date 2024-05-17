import SubPage from "../SubPage.js"
import { tourResultPage } from "./TourResultPage.js"
import { resultListInfo, resultDetailInfo } from "../../models/Info.js"

class ResultListSubpage extends SubPage {
    $dv;

    init() {
        this.$elem.innerHTML = `
            <h2>토너먼트 결과</h2>
            <div id="result_sub_area"></div>
        `;

        this.$dv = $elem.querySelector("#result_sub_area");
        resultListInfo.sendData = null;
        async () => {
            try {
                await resultListInfo.requestAPI();
                // for(let i = 0; i < resultListInfo.recvData.length; i++)
                // {
                //     this.$dv.innerHTML += `
                //     <div>
                //      <button id=${resultListInfo.recvData[i].tournamentID}>${resultListInfo.recvData[i].date}</button>
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
        // for (let i = 0; i < resultListInfo.recvData.length; i++)
        // {
        //     let temp = this.$dv.querySelector("${resultListInfo.recvData[i].tournamentID}");
        //     temp.addEventListener("click", () => {
        //         resultDetailInfo.sendData.tournamentID = resultListInfo.recvData[i].tournamentID;
        //         this.requestShift("result_detail_subpage");
        //     });
        // }
    }
}

export const resultListSubpage = new ResultListSubpage(
    tourResultPage.$elem.querySelector("div"),
    tourResultPage,
    null,
    "result_list_subpage",
)