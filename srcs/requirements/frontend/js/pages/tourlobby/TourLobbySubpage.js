import SubPage from "../SubPage.js";
import { tourLobbyInfo } from "../../models/Info.js";

/**
 * TourLobbySubpage -> TourGameLoungeSubpage
 * 이렇게 shift할 경우에는 소켓이 살아 있어야 한다.
 * 나머지 shift의 경우에는 소켓.close() 해 주어야 함.
 * 
 * 1. TourLobbySubpage와 TourGameLoungeSubpage 에다가 sock 변수를 각각 만든다
 *    -> 너무 별로인듯..
 * 2. TourLobbyPage에다가 sock 변수를 만든다.
 *    - TourLobbySubpage <---> TourGameLoungeSubpage 간의 shift -> sock 유지
 *    - 나머지 shift -> sock.close();
 */

class TourLobbySubpage extends SubPage {
    sock;
    $title;
    $players;
    $exitBtn;
    $readyBtn;
    $startBtn;

    init() {
        this.$elem.innerHTML = `
            <h2></h2>
            <ol></ol>
            <button id="tour-ready">준비</button>
            <button id="tour-start">시작</button>
            <button id="tour-exit">토너먼트 나가기</button>
        `;

        /**
         * 만약 현재 플레이어가 방장이 아닌 경우 -> readyBtn 활성화시킴. (class="none")
         * readyBtn: 백에게 현재 준비상태가 완료되었다고 API 전송.
         * 만약 현재 플레이어가 방장인 경우 -> startBtn 활성화시킴. (class="none")
         * startBtn: 모든 플레이어가 준비상태가 된 경우 백에서 이 버튼을 활성화시킴.
         * 활성화된 startBtn: 백에게 시작하라고 API 전송.
         * -> 백은 모든 플레이어들에게 시작한다는 API 전송.
         */

        this.$title = this.$elem.querySelector("h2");
        this.$players = this.$elem.querySelector("ol");
        this.$readyBtn = this.$elem.querySelector("#tour-ready");
        this.$startBtn = this.$elem.querySelector("#tour-start");
        this.$exitBtn = this.$elem.querySelector("#tour-exit");

        /**
         * 만약 새 탭이나 새로고침을 한 경우 이 subpage로 넘어오게 되어 자동으로 소켓이 생성된다. (중복 시 소켓 연결 거절)
         * 여기서 소켓을 생성한다.
         * 소켓의 비동기 처리에 대한 eventListener들을 모두 등록한다.
         * try {
         *     this.sock = new Websocket("uri");
         * }
         * catch {
         *     this.requestShift("main_page");
         * }
         * 실패했을 경우 main_page로 쫓아내야 함.
         * this.sock.addEventListener("message", (event) => {
         *     
         * })
         * window.addEventListener("beforeunload", this.sock.close);
         */

        this.$exitBtn.addEventListener("click", () => {
            this.requestShift("tour_list_subpage");
        });
    }

    fini() {
        /**
         * 윗 주석에 상세 설명 적혀있음.
         * if문으로 sock.close()를 해야 할 지 결정해야 할 듯.
         * this.sock.close();
         */
        this.$elem.innerHTML = ``;
    }
};