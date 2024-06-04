import Page from "./Page.js";
import { rootPage } from "./RootPage.js";
import { meAPI } from "../models/API.js"

export default class SubPage extends Page {
    childShift(nextChildName) {}

    route(nextChildName) {
        // try-catch로 짜야 하나?
        this.requestShift(nextChildName);
        history.pushState(null, null, location.origin + location.pathname + "#" + nextChildName);
    }

    mount(childName, initFunc, finiFunc) {}

    // login, signup 서브 페이지를 제외한 모든 서브페이지 init 시마다 유효한 액세스인지 확인 필수!
    async validate() {
        try {
            await meAPI.request();
        }
        catch {
            alert("Cannot Access!");
            location.reload();
        }
    }

    init() {
    }

    fini() {
        
    }
};
