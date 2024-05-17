import SubPage from "../SubPage.js"
import { tourResultPage } from "./TourResultPage.js"

class ResultDetailSubpage extends SubPage {
    $dv;

    init() {
        this.$elem.innerHTML = `
            <h2>토너먼트 결과</h2>
            <div id="result_sub_area"></div>
        `;
        this.$dv = this.$elem.querySelector("#result_sub_area");
        async() => {
            try {
                await resultDetailInfo.requestAPI();
                // for(let i = 0; i < resultDetailInfo.recvData.length; i++)
                // {
                //     this.$dv.innerHTML += `
                //         <div>
                //             <button>${resultDetailInfo.recvData[i].rank} : ${resultDetailInfo.recvData[i].playerName}</button>
                //         </div>
                //     `;
                // }
            }
            catch(e) {
                alert(`Result Detail: ${e.message}`);
                this.requestShift("result_list_subpage");
            }
        }
    }

    fini() {
        this.$elem.innerHTML =``;
    }
}

export const resultDetailSubpage = new ResultDetailSubpage(
    tourResultPage.$elem.querySelector("div"),
    tourResultPage,
    null,
    "result_detail_subpage",
);