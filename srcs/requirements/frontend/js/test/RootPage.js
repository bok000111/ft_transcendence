//ex) tournament room page
export default class RootPage extends Component {
    parent; // object
    initSubpageName; // string
    curSubpage; // object
    subpage = {};

    constructor(elem, parent, initSubpageName, pageName, eventInfo) {
        super(elem);
        this.initSubpageName = initSubpageName;
        if (parent)
            parent.mount(pageName, this.init.bind(this), this.fini.bind(this), eventInfo);
    }

    mount(subpageName, initFunc, finiFunc, eventInfo) {
        this.subpage[subpageName] = {
            init: initFunc,
            fini: finiFunc,
        }
        if (eventInfo) {
            eventInfo.forEach(({ $elem, event, handler }) => {
                $elem.addEventListener(event, handler);
            });
        }
        if (subpageName === this.initSubpageName)
            this.curSubpage = this.subpage[subpageName];
    }

    shift(nextSubpage) {
        this.curSubpage.$elem.classList.add("none");
        this.curSubpage.fini();
        this.curSubpage = this.subpage[nextSubpage];
        this.curSubpage.init();
        this.curSubpage.$elem.classList.remove("none");
    }

    init() {
        this.initSubpageName.init();
    }
    fini() {
        this.shift(initSubpageName);
    }
};

export const rootPage = new RootPage(document.body, null, "admin", null);