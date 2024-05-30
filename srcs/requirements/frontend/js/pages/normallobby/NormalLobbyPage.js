import Page from "../Page.js";
import { rootPage } from "../RootPage.js";

class NormalLobbyPage extends Page {
    $mainBtn;

    setup() {
        this.$mainBtn = this.$elem.querySelector("button");
    }

    setEvent() {
        this.$mainBtn.addEventListener("click", () => {
            this.requestShift("main_page");
        });
    }
};

const normalLobbyPage = new NormalLobbyPage(
    rootPage.$elem.querySelector(".normal-lobby-page"),
    rootPage,
    "normal_list_subpage",
    "normal_lobby_page"
);