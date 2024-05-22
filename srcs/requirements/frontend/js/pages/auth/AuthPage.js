import { rootPage } from "../RootPage.js";
import Page from "../Page.js";

export const authPage = new Page(
    rootPage.$elem.querySelector(".auth-page"),
    rootPage,
    "login_subpage",
    "auth_page"
);