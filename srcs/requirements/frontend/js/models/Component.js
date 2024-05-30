export default class Component {
    $elem;

    constructor(elem) {
        this.$elem = elem;
        this.setup();
    }
    setup() {}
};