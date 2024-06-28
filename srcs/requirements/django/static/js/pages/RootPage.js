import Component from "../models/Component.js";

export default class RootPage extends Component {
    static sock = null;
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

    async init() {
        await this.curChild.curChild.route("auth_page/login_subpage", true);

        document.querySelector("#titlePong").addEventListener("click", (event) => {
            event.preventDefault();
            this.curChild.curChild.route("main_page/main_subpage");
        });
        window.addEventListener("popstate", () => {
            // 컴파일 에러 안 나나? 안 나면 다행이고.
            this.curChild.curChild.route(location.pathname.substring(1), true);
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