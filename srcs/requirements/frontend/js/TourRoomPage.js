import Page from "./Page.js";
import { tourRoomInfo } from "./Info.js";

class TourRoomPage extends Page {
    $to_main
    $to_list
    interval;

    setup() {
        this.mount("tour_room_page");
        this.$to_main = this.$elem.querySelector("#to-main");
        this.$to_list = this.$elem.querySelector("#to-list");
    }

    setEvent() {
        this.$to_main.addEventListener("click", () => {
            this.shift("main_page");
        });
        this.$to_list.addEventListener("click", () => {
            this.shift("tour_list_page");
        });
    }

    renderPlayers({ list }) {

    }

    init() {
        /**
         * 백에게 방에 접속한다는 API 전송
         * 주기적으로 방에 대한 정보를 받는다.
         */
    }

    fini() {
        /**
         * 백에게 방에서 나간다는 API 전송
         * 
         */
        clearInterval(interval);
        this.$elem.lastChild.remove();
    }
};