import Page from "../Page.js";
import { rootPage } from "../RootPage.js";

class TourLobbyPage extends Page {
    sock;
    $mainBtn;

    setup() {
        this.sock = null;
        this.$mainBtn = this.$elem.querySelector("button");
    }

    setEvent() {
        this.$mainBtn.addEventListener("click", () => {
            this.requestShift("main_page");
        });
    }
};

export const tourLobbyPage = new TourLobbyPage(
    rootPage.$elem.querySelector(".tour-lobby-page"),
    rootPage,
    "tour_list_subpage",
    "tour_lobby_page"
);