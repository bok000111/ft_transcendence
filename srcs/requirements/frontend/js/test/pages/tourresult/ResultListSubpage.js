import SubPage from "../SubPage.js"
import { tourResultPage } from "./TourResultPage.js"

class ResultListSubpage extends SubPage {
    init() {
        /*
        let resultFromServer = (); // 서버로부터 리스트 가져옴.
        this.$elem.innerHTML = `
            // 아직 명세에 관한 부분이 없어서 임시로 작성. 예외적으로 여기에서 eventListener 달아줘야할 것 같음.
            // 어떻게 주는진 모르겠지만 확실히 개별 결과에 대해서 구분할 수있는 ID 등을 사용해서 리스트 요소에 넣어줘야함.
            // 각각에 대해서 resultDetail 페이지로 넘어갈 수 있도록 addeventListener 추가예정.
            // 받아와서 생성된 버튼에 대해서 각각 addEventListener를 어떻게 넣어줘야할지 모르겠음..
            ${resultFromServer.map(item => `<li id="tmp"><button>${item}</button></li>`).join('')}
            // 위 코드를 forEach나 for문으로 수정 후, addEventListener로 requestShift 호출하도록 해야함.
        `;
        */
    }

    fini() {
        this.$elem.innerHTML = ``;
    }
}

export const resultListSubpage = new ResultListSubpage(
    tourResultPage.$elem.querySelector("div"),
    tourResultPage,
    null,
    "result_list_subpage",
)