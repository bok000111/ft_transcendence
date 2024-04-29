import PageShifter from "./PageShifter.js";
import Component from "./Component.js";

export default class Page extends Component {
    setup() {
        PageShifter.mount(pageName, this.$elem, this.init.bind(this), this.fini.bind(this));
    }
    shift(nextPage) {
        PageShifter.shift(nextPage);
    }
    init() {}
    fini() {}
};