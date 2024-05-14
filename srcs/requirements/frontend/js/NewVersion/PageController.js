class PageController {
    #pages = {};
    $currentPage;

    static mount(pageName, elem, initFunc, finiFunc) {
        this.#pages[pageName] = {
            $elem: elem,
            init: initFunc, // 얘는 없어질 수도 있다.
            fini: finiFunc,
        };
        if (pageName === "login_page") {
            this.$currentPage = this.#pages[pageName];
        }
    }

    /**
     * use example: PageController.shift("login_page");
     * 내부 함수호출 순서는 나름대로 렌더링 순서를 고려해서 짜긴 했음..
     */
    static shift(nextPage) {
        this.$currentPage.$elem.classList.add("none");
        this.#pages[nextPage].init();
        this.#pages[nextPage].$elem.classList.remove("none");
        this.$currentPage.fini();
        this.$currentPage = this.#pages[nextPage];
    }
};

const pageController = new PageController();
const subpageController = new PageController();