import Component from "../models/Component.js";
import { meAPI } from "../models/API.js";
import { info } from "../models/Info.js";

export default class RootPage extends Component {
    parent; // object
    initChildName; // string
    curChild; // object
    selfName;
    child = {};

    constructor(elem, parent, initChildName, selfName) {
        super(elem);
        this.initChildName = initChildName;
        this.parent = parent;
        this.selfName = selfName;
        if (parent)
            parent.mount(this, selfName);
        this.setEvent();
    }

    setEvent() {}

    mount(child, childName) {
        this.child[childName] = child;
        if (childName === this.initChildName) {
            this.curChild = this.child[childName];
        }
    }

    requestShift(nextChildName) {}

    childShift(nextChildName) {
        this.curChild.fini();
        this.curChild = this.child[nextChildName];
        this.curChild.init();
    }

    getHashURL() {
        return this.curChild.selfName + "/" + this.curChild.curChild.selfName;
    }

    async checkLoggedIn() {
        try {
            await meAPI.request();
            info.myID = meAPI.recvData.data.user.id;
            info.myUsername = meAPI.recvData.data.user.username;
            this.curChild = this.child["main_page"];
            const url = location.origin + location.pathname + '#' + this.getHashURL();
            history.replaceState(null, null, url);
        }
        catch {
            const url = location.origin + location.pathname + '#' + this.getHashURL(); // 일단은 항상 로그인 안한 오류에 대해서만. 나중에 메인문에서 뒤로 갈 때 고려해야함.
            history.replaceState(null, null, url);
        }
    }

    async pongHandler() {
        /**
         * 로그인 세션이 유지되는 상태
         * -> 로그인 상태 : 메인 화면
         * -> 나머지 : 로그인 페이지
         */
        await this.checkLoggedIn();
        this.curChild.init();
    }

    async init() {
        await this.pongHandler();
        const title_pong = document.querySelector("#titlePong");

        title_pong.addEventListener("click", (event) => {
            event.preventDefault();
            location.reload(location);
        });
        window.addEventListener("popstate", () => {
            // 컴파일 에러 안 나나? 안 나면 다행이고.
            this.curChild.curChild.requestShift(location.hash.substring(1));
        });
    }

    // async route() {
    //     if (location.hash === "#login_subpage") {
    //         try {
    //             await meAPI.request();
    //         }
    //         catch {
    //             const url = location.origin + location.pathname + '#' + "login_subpage"; // 일단은 항상 로그인 안한 오류에 대해서만. 나중에 메인문에서 뒤로 갈 때 고려해야함.
    //             history.pushState(null, null, url);
    //         }
    //     }
    //     switch(location.hash) {
    //         case "#login_subpage":
    //             this.childShift("auth_page");
    //             this.curChild.childShift("login_subpage");
    //             break;
    //         case "#signup_subpage":
    //             this.childShift("auth_page");
    //             this.curChild.childShift("signup_subpage");
    //             break;
    //         case "#main_subpage":
    //             this.childShift("main_page");
    //             this.curChild.childShift("main_subpage");
    //         default:
    //             alert("Cannot Access!");
    //             location.reload();
    //             break;
    //     }
    // }

    fini() {}
};

// we should call rootPage.init(); in main.js
export const rootPage = new RootPage(document.body, null, "auth_page", "root");

// rootPage 초기화
// page 초기화
// subPage 초기화
// rootpage에 page mount
// 각 페이지에 gak subpage mount