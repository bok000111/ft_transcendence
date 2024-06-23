import { rootPage } from "../RootPage.js";
import Page from "../Page.js";

export const gamePage = new Page(
    rootPage.$elem.querySelector(".game-page"),
    rootPage,
    "pong_subpage",
    "game_page"
);