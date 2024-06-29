import Page from "./Page.js";
import { meAPI } from "../models/API.js"
import { info } from "../models/Info.js";

export default class SubPage extends Page {
    childShift(nextChildName) {}

    async route(nextChildName, replace = false) {
        /**
         * auth_fail인 경우 auth_page/login_subpage 로 route
         * auth_success인 경우 정상적으로 route
         */
        const page_path = nextChildName.split("/")[0];
        try {
            await meAPI.request();
            info.myID = meAPI.recvData.data.user.id;
            info.myUsername = meAPI.recvData.data.user.username;
            if (page_path === "auth_page") {
                alert("already logged in");
                nextChildName = "main_page/main_subpage";
            }
        }
        // 로그인이 안 된 경우
        catch {
            if (page_path !== "auth_page") {
                if (this.selfName !== "login_subpage" && this.selfName != "signup_subpage")
                    alert("login required");
                nextChildName = "auth_page/login_subpage";
            }
        }
        this.requestShift(nextChildName);
        if (replace) {
            history.replaceState(null, null, location.origin + "/" + nextChildName);
        }
        else if (location.pathname.substring(1) !== nextChildName) {
            history.pushState(null, null, location.origin + "/" + nextChildName);
        }
    }

    mount(childName, initFunc, finiFunc) {}

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
