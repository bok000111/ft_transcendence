import Page from "./Page.js";
import { meAPI } from "../models/API.js"

export default class SubPage extends Page {
    childShift(nextChildName) {}

    requestShift(nextChildName) {
        this.parent.childShift(nextChildName);
    }

    mount(childName, initFunc, finiFunc) {}

    // login, signup 서브 페이지를 제외한 모든 서브페이지 init 시마다 유효한 액세스인지 확인 필수!
    async vailidate() {
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
