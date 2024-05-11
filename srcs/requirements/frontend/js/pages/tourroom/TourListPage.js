import Page from "../Page.js";
import { tourListInfo, tourRoomInfo } from "../../models/Info.js";

class TourRoomPage extends Page {
    $mainBtn;
    subPage;

    setup() {
        this.$mainBtn = this.$elem.querySelector("#to-main");
    }
    setEvent() {
        this.$mainBtn.addEventListener("click", () => {
            this.pageShifter.shift("main_page");
        });
    }
    shift(nextPage) {

    }
    init() {
        this.subPage.init();
    }
    fini() {
        this.subPage.fini();
        this.subPage = defaultSubPage;
    }
}

class TourListSubpage {
    parent;

    subShift(nextPage) {
        this.fini();
        nextPage.init();
    }
}






















class TourListPage extends Page {
    $to_main;
    interval;

    setup() {
        this.mount("tour_list_page");
        this.$to_main = this.$elem.querySelector("#to-main");
    }

    setEvent() {
        this.$to_main.addEventListener("click", () => {
            this.shift("main_page");
        });
    }

    // list 내부에는 roomNum, roomName, curNum, maxNum
    renderList({ list }) {
        const ul = document.createElement("ul");

        for (elem of list) {
            const newNode = document.createElement("li")

            newNode.innerHTML = `
                <h3>${elem.roomName}</h3>
                <h3>${elem.peopleNum}/${elem.peopleMax}</h3>
            `;
            newNode.addEventListener("click", () => {
                /** 
                 * tourRoomInfo의 roomNum 값을 바꾸어 주는 부분 필요.
                 * 그래야 TourRoomPage에서 init() 해 줄 때 바뀐 roomNum을 기반으로
                 * API 요청 후 room에 대한 정보를 가져올 수 있다.
                 */
                tourRoomInfo.sendData.roomNum = elem.roomNum; // 이렇게 써도 되나? 아직도 클로저 잘 모르겠음..
                this.shift("tour_entry_page");
            });
            ul.appendChild(newNode);
        }
        this.$elem.appendChild(ul);
    }

    init() {
        this.startInterval(async () => {
            try {
                await tourListInfo.requestAPI();
                this.renderList(tourListInfo.recvData);
            }
            catch (e) {
                alert(`Tournament List: ${e.message}`);
            }
        }, 3000, this.interval);
    }

    fini() {
        clearInterval(this.interval);
        this.$elem.lastChild.remove();
    }
};