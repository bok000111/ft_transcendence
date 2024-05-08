import Page from "./Page.js";

class TourEntryPage extends Page {
    $to_main;
    $to_list;
    $form;

    setup() {
        this.mount("tour_entry_page");
        this.$to_main = this.$elem.querySelector("#to-main");
        this.$to_list = this.$elem.querySelector("#to-list");
        this.$form = this.$elem.querySelector("form");
    }

    setEvent() {
        this.$to_main.addEventListener("click", () => {
            this.shift("main_page");
        });
        this.$to_list.addEventListener("click", () => {
            this.shift("tour_list_page");
        });
        this.$form.addEventListener("submit", (event) => {
            event.preventDefault();
        });
    }

    init() {

    }

    fini() {
        this.$form.querySelector("#nickname").value = "";
    }
}