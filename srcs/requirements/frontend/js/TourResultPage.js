import Page from "./Page.js"
import { tourResultInfo } from "./Info.js"

class TourResultPage extends Page {
   $resultList;
   $homeBtn;

   setup() {
        this.mount("tour_result_page");
        this.$homeBtn = this.$elem.querySelector("home");
        this.$resultList = this.$elem.querySelector("#resultList");
   }

   setEvent() {
        this.$homeBtn.addEventListener("click", () => {
            this.shift("main_page");
        });
        // list 관련 일단 애매해서 냅둠. 어쩌면 이 페이지는 각 element 들에 대해서 init에서 해줘야 할 수도?
   }

   init() {
        const resultFromServer = tourResultInfo();
        this.$resultList.innerHTML = `
            // 아직 명세에 관한 부분이 없어서 임시로 작성. 예외적으로 여기에서 eventListener 달아줘야할 것 같음.
            // 어떻게 주는진 모르겠지만 확실히 개별 결과에 대해서 구분할 수있는 ID 등을 사용해서 리스트 요소에 넣어줘야함.
            // 각각에 대해서 resultDetail 페이지로 넘어갈 수 있도록 addeventListener 추가예정.
            // 받아와서 생성된 버튼에 대해서 각각 addEventListener를 어떻게 넣어줘야할지 모르겠음..
            ${resultFromServer.map(item => `<li id="tmp"><button>${item}</button></li>`).join('')}
        `;
   }

   fini() {
        this.$resultList.innerHTML = ``;
   }
}