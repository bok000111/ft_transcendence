/**
 * static class로 구현
 * 각 페이지에서 PageShifter.mount()를 호출함으로써 PageShifter에 등록한다.
 * 페이지가 바뀔 때 마다 등록되어 있는 함수들이 같이 호출된다.
 */

class PageShifter {
    pages = {};
    initPage;
    $currentPage; // !??!

    constructor(initPage) {
        this.initPage = initPage;
    }

    mount(pageName, elem, initFunc, finiFunc) {
        this.pages[pageName] = {
            $elem: elem,
            init: initFunc, // 얘는 없어질 수도 있다.
            fini: finiFunc,
        };
        if (pageName === this.initPage)
            this.$currentPage = this.pages[pageName];
    }

    /**
     * use example: PageShifter.shift("login_page");
     * 내부 함수호출 순서는 나름대로 렌더링 순서를 고려해서 짜긴 했음..
     */
    shift(nextPage) {
        this.$currentPage.$elem.classList.add("none");
        this.pages[nextPage].init();
        this.pages[nextPage].$elem.classList.remove("none");
        this.$currentPage.fini();
        this.$currentPage = this.pages[nextPage];
    }
};

export const page_shifter = new PageShifter("login_page");