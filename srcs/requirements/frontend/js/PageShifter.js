/**
 * static class로 구현
 * 각 페이지에서 PageShifter.mount()를 호출함으로써 PageShifter에 등록한다.
 * 페이지가 바뀔 때 마다 등록되어 있는 함수들이 같이 호출된다.
 */

export default class PageShifter {
    static #pages = {};
    static #$current_page;

    static mount(pageName, elem, initFunc, finiFunc) {
        this.#pages[pageName] = {
            $elem: elem,
            init: initFunc, // 얘는 없어질 수도 있다.
            fini: finiFunc,
        };
        if (pageName === "login_page") {
            this.#$current_page = this.#pages[pageName];
        }
    }

    /**
     * use example: PageShifter.shift("login_page");
     * 내부 함수호출 순서는 나름대로 렌더링 순서를 고려해서 짜긴 했음..
     */
    static shift(nextPage) {
        this.#pages[nextPage].init();
        this.#$current_page.$elem.classList.add("none");
        this.#pages[nextPage].$elem.classList.remove("none");
        this.#$current_page.fini();
        this.#$current_page = this.#pages[nextPage];
    }
};