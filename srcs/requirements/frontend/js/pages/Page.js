import { PageShifter } from "../shifters/PageShifter.js";
import { SubpageShifter } from "../shifters/SubpageShifter.js";
import Component from "../models/Component.js";

export default class Page extends Component {
    pageShifter;
    /**
     * 자식 클래스 setup() 메소드에서  mount() 함수를 호출해야 한다.
     * ex) this.mount("login_page");
     */
    constructor(pageShifter, pageName) {
        this.pageShifter = pageShifter;
        this.pageShifter.mount(pageName, this.$elem, this.init.bind(this), this.fini.bind(this));
    }
    shift(nextPage) {
        this.pageShifter.shift(nextPage);
    }
    startInterval(callback, time, interval) {
        callback();
        interval = setInterval(callback, time);
    }
    init() {}
    fini() {}
};