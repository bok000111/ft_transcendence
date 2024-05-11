import { PageShifter } from "../shifters/PageShifter.js";
import { SubpageShifter } from "../shifters/SubpageShifter.js";
import Component from "../models/Component.js";

export default class Page extends Component {
    pageShifter;

    constructor(elem, pageShifter, pageName) {
        super(elem);
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