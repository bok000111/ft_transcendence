//ex) tournament room page
export default class RootPage extends Component {
    parent; // object
    initChildName; // string
    curChild; // object
    child = {};

    constructor(elem, parent, initChildName, selfName) {
        super(elem);
        this.initChildName = initChildName;
        if (parent)
            parent.mount(selfName, this.init.bind(this), this.fini.bind(this));
    }

    mount(childName, initFunc, finiFunc) {
        this.child[childName] = {
            init: initFunc,
            fini: finiFunc,
        }
        if (childName === this.initChildName)
            this.curChild = this.child[childName];
    }

    requestShift(nextChild) {}

    childShift(nextChild) {
        this.curChild.$elem.classList.add("none");
        this.curChild.fini();
        this.curChild = this.child[nextChild];
        this.curChild.init();
        this.curChild.$elem.classList.remove("none");
    }
    
    init() {
        this.child[initChildName].init();
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