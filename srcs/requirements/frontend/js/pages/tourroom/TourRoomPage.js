import Page from "../Page.js";
import { rootPage } from "../RootPage.js";

class TourRoomPage extends Page {
    $btn;

    setup() {
        this.$btn = this.$elem.querySelector("button");
    }

    setEvent() {
        this.$btn.addEventListener("click", () => {
            this.requestShift("main_page");
        });
    }
};

const tourRoomPage = new TourRoomPage(
    rootPage.$elem.querySelector(".tour-room-page"),
    rootPage,
    "tour_list_subpage",
    "tour_room_page"
);