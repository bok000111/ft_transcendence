import { rootPage } from "../RootPage.js";

const authPage = new Page(
    rootPage.$elem.querySelector(".auth-page"),
    rootPage,
    "login_subpage",
    "auth_page"
);