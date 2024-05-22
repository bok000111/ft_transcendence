import Page from "./Page.js";

export default class SubPage extends Page {
    childShift(nextChildName) {}

    mount(childName, initFunc, finiFunc) {}

    init() {
        //서버로부터 응답 받아서 DOM요소 정리 슥삭
        //~.innerHTML = `ㅁㄴㅇㄹ`; // ㅁㄴㅇㄹ에 띄울애들 정리
    }

    fini() {
        
    }
};
