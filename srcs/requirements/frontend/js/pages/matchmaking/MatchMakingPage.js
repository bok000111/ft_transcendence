import Page from "../Page.js";
import { rootPage } from "../RootPage.js";

class MatchMakingPage extends Page {
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

const matchMakingPage = new MatchMakingPage(
    rootPage.$elem.querySelector(".match-making-page"),
    rootPage,
    "match_making_subpage",
    "match_making_page"
);