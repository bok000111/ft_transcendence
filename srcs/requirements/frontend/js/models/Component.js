export default class Component {
    $elem;

    constructor(elem) {
        this.$elem = elem;
        this.setup();
        this.setEvent();
    }
    setup() {}
    setEvent() {}
};