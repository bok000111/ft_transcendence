import Page from "../Page.js";
import { rootPage } from "../RootPage.js";

class TourLobbyPage extends Page {
    sock;

    setup() {
        this.sock = null;
    }
};

export const tourLobbyPage = new TourLobbyPage(
    rootPage.$elem.querySelector(".tour-lobby-page"),
    rootPage,
    "tour_list_subpage",
    "tour_lobby_page"
);