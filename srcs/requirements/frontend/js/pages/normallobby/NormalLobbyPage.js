import Page from "../Page.js";
import { rootPage } from "../RootPage.js";

class NormalLobbyPage extends Page {
    sock;

    setup() {
        this.sock = null;
    }
};

export const normalLobbyPage = new NormalLobbyPage(
    rootPage.$elem.querySelector(".normal-lobby-page"),
    rootPage,
    "normal_list_subpage",
    "normal_lobby_page"
);