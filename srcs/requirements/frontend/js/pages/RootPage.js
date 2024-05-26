import Component from "../models/Component.js";
import { meAPI } from "../models/API.js";
import { info } from "../models/Info.js";

export default class RootPage extends Component {
    parent; // object
    initChildName; // string
    curChild; // object
    child = {};

    constructor(elem, parent, initChildName, selfName) {
        super(elem);
        this.initChildName = initChildName;
        this.parent = parent;
        if (parent)
            parent.mount(this, selfName);
    }

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
    
    async checkLoggedIn() {
        try {
            await meAPI.request();
            info.username = meAPI.recvData.data.user.username;
            rootPage.childShift("main_page");
        }
        catch {
            
        }
    }

    init() {
        /**
         * 로그인 세션이 유지되는 상태
         * -> 토너먼트 진행중 : 토너먼트 화면
         * -> 나머지 : 메인 화면
         */
        this.child[this.initChildName].init();
    }

    fini() {}
};

// we should call rootPage.init(); in main.js
export const rootPage = new RootPage(document.body, null, "auth_page", "root");

// rootPage 초기화
// page 초기화
// subPage 초기화
// rootpage에 page mount
// 각 페이지에 gak subpage mount