import PageShifter from "./PageShifter.js";

export default class Page {
    $elem;
    constructor(elem, pageName) {
        this.$elem = elem;
        PageShifter.mount(pageName, this.$elem, this.init.bind(this), this.fini.bind(this));
    }
    shift(nextPage) {
        PageShifter.shift(nextPage);
    }
    init() {}
    fini() {}
};