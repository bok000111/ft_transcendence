import { rootPage } from "../RootPage.js"
import Page from "../Page.js"

// 추가로 다른 "페이지" 추가해야함. (for shift)

export default class MainPage extends Page {
    $logoutBtn;
    $participateBtn;
    $tournamentResultBtn;
    $matchmakingBtn;

    constructor(elem, parent, selfName) {
        super(elem);
        this.setEvent();
        if (parent)
            parent.mount(selfName, this.init.bind(this), this.fini.bind(this));
    }

    init() {} // no need to init

    fini() {} // no need to deinit

    setEvent() {
        this.$logoutBtn = document.querySelector("#logout");
        this.$participateBtn = document.querySelector("#participate");
        this.$tournamentResultBtn = document.querySelector("#tournamentResult");
        this.$matchmakingBtn = document.querySelector("#matchmaking");

        this.$logoutBtn.addEventListener("click", ); // logoutAPI sending func should be added
        this.$participateBtn.addEventListener("click", requestShift(tourRoom)); // 나중에 인자 이름 체킹 필요
        this.$tournamentResultBtn.addEventListener("click", requestShift(tourResult)); // 나중에 인자 이름 체킹 필요
        this.$matchmakingBtn.addEventListener("click", requestShift(matchMaking)); // 나중에 인자 이름 체킹 필요
    }
}

export const mainPage = new MainPage(
    rootPage.$elem.querySelector("main-page"),
    rootPage,
    "main_page",
);