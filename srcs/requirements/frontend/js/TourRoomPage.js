import Page from "./Page.js";
import { tourListInfo, tourRoomInfo } from "./Info.js";

class TourRoomPage extends Page{
    $frame;
    interval;

    setup() {
        this.mount("tour_room_page");
        this.$frame = this.$elem.querySelector("div");
    }

    renderList(data) {

    }

    renderRoom(data) {

    }

    init() {
        interval = setInterval(
            
        );
    }

    fini() {
        clearInterval(interval);
    }
};