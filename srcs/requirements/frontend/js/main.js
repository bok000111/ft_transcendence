import { rootPage } from "./pages/RootPage.js";
import { loginSubpage } from "./pages/auth/LoginSubpage.js";
import { signupSubpage } from "./pages/auth/SignupSubpage.js";
import { mainSubpage } from "./pages/main/MainSubpage.js";
import { normalEntrySubpage } from "./pages/normallobby/NormalEntrySubpage.js";
import { normalListSubpage } from "./pages/normallobby/NormalListSubpage.js";
import { normalLobbySubpage } from "./pages/normallobby/NormalLobbySubpage.js";
import { normalMakeSubpage } from "./pages/normallobby/NormalMakeSubpage.js";

rootPage.init();

const title_pong = document.querySelector("#titlePong");

title_pong.addEventListener("click", () => {
    rootPage.fini();
    rootPage.curChild.curChild.fini(); // SubPage innerHTML clear
    rootPage.curChild.fini();
    rootPage.init();
});