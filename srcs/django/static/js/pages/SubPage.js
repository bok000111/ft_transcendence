import Page from "./Page.js";
import { meAPI } from "../models/API.js"
import { info } from "../models/Info.js";

export default class SubPage extends Page {
    childShift(nextChildName) { }

    async route(nextChildName, replace = false) {
        /**
         * auth_fail인 경우 auth_page/login_subpage 로 route
         * auth_success인 경우 정상적으로 route
         */
        const page_path = nextChildName.split("/")[0];
        nextChildName = "auth_page/login_subpage";
        const access_token_from_url = new URLSearchParams(window.location.hash.slice(1)).get("access_token");
        if (access_token_from_url) {
            window.localStorage.setItem("access_token", access_token_from_url);
            window.location.hash = "";
        }
        if (window.localStorage.getItem("access_token")) {
            await meAPI.request().then(() => {
                info.myID = meAPI.recvData.data.user.id;
                info.myUsername = meAPI.recvData.data.user.username;
                nextChildName = "main_page/main_subpage";
            }).catch(() => { nextChildName = "auth_page/login_subpage"; });
        }
        this.requestShift(nextChildName);
        if (replace) {
            history.replaceState(null, null, location.origin + "/" + nextChildName);
        }
        else if (location.pathname.substring(1) !== nextChildName) {
            history.pushState(null, null, location.origin + "/" + nextChildName);
        }
    }

    mount(childName, initFunc, finiFunc) { }

    // login, signup 서브 페이지를 제외한 모든 서브페이지 init 시마다 유효한 액세스인지 확인 필수!
    // async validate() {
    //     try {
    //         await meAPI.request();
    //     }
    //     catch {
    //         alert("Cannot Access!");
    //         location.reload(true);
    //     }
    // }

    init() {
    }

    fini() {

    }
};
