import SubPage from "../SubPage.js"
import { tourResultPage } from "./TourResultPage.js"
import { tourResultDetailAPI } from "../../models/API.js"

class TourResultDetailSubpage extends SubPage {
    $dv;

    init() {
        this.$elem.innerHTML = `
            <h2>토너먼트 결과</h2>
            <div id="result_sub_area"></div>
        `;
        this.$dv = this.$elem.querySelector("#result_sub_area");
        async() => {
            try {
                await tourResultDetailAPI.request();
                // for(let i = 0; i <tourResultDetailAPI.recvData.length; i++)
                // {
                //     this.$dv.innerHTML += `
                //         <div>
                //             <button>$tourResultDetailAPI.recvData[i].rank} : $tourResultDetailAPI.recvData[i].playerName}</button>
                //         </div>
                //     `;
                // }
            }
            catch(e) {
                alert(`Result Detail: ${e.message}`);
                this.requestShift("tour_result_list_subpage");
            }
        }
    }

    fini() {
        this.$elem.innerHTML =``;
    }
}

export const resultDetailSubpage = new TourResultDetailSubpage(
    tourResultPage.$elem.querySelector("div"),
    tourResultPage,
    null,
    "tour_result_detail_subpage",
);