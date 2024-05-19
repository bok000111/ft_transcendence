import SubPage from "../SubPage.js";
import { tourLobbyInfo } from "../../models/Info.js";

class TourLobbySubpage extends SubPage {
    sock;
    $title;
    $ol;
    $btn;

    init() {
        this.$elem.innerHTML = `
            <h2></h2>
            <ol></ol>
            <button>토너먼트 나가기</button>
        `;

        this.$title = this.$elem.querySelector("h2");
        this.$ol = this.$elem.querySelector("ol");
        this.$btn = this.$elem.querySelector("button");

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

        this.$btn.addEventListener("click", () => {
            this.requestShift("tour_list_subpage");
        });
    }

    fini() {
        this.$elem.innerHTML = ``;
    }
};