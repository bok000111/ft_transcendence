import { auth } from "../Page.js";
import SubPage from "../SubPage.js";

class LoginSubpage extends SubPage {
    init() {
        this.$elem.innerHTML = `
            <form>
                <input id="email" type="text" placeholder="email">
                <input id="password" type="text" placeholder="password">
                <input type="submit" value="login">
            </form>
            <button>signup</button>
        `;
    }
    
    fini() {

    }
};

const loginSubpage = new LoginSubpage(
    auth.$elem.querySelector("div"),
    auth,
    null,
    "login_subpage",
    null
);