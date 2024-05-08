import PageShifter from "./PageShifter.js";
import Component from "./Component.js";

export default class Page extends Component {
    /**
     * 자식 클래스 setup() 메소드에서  mount() 함수를 호출해야 한다.
     * ex) this.mount("login_page");
     */
    mount(pageName) {
        PageShifter.mount(pageName, this.$elem, this.init.bind(this), this.fini.bind(this));
    }
    shift(nextPage) {
        PageShifter.shift(nextPage);
    }
    startInterval(callback, time, interval) {
        callback();
        interval = setInterval(callback, time);
    }
    init() {}
    fini() {}
};