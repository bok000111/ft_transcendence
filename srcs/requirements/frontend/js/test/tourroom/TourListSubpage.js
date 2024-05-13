import SubPage from "../SubPage.js";
import { tourListInfo, tourRoomInfo } from "../../models/Info.js";

class TourListSubpage extends SubPage {
    interval;
    $ul;
    $btn;

    startInterval(time, callback) {
        callback();
        this.interval = setInterval(callback, time);
    }

    /**
     * list = list of objects constructed by
     * {
     *     roomID,
     *     roomName,
     *     curNum,
     *     maxNum
     * }
     */
    renderList({ list }) {
        this.$ul.innerHTML = ``;

        for (elem of list) {
            const newNode = document.createElement("li");

            newNode.innerHTML = `
                <h3>${elem.roomName}</h3>
                <h3>${elem.curNum}/${elem.maxNum}</h3>
            `;
            newNode.addEventListener("click", () => {
                // 클로저의 성질을 잘 몰라서 얘는 될 지 모르겠다..
                tourRoomInfo.sendData[roomID] = elem.roomID;
                this.requestShift("tour_entry_subpage");
            });
            this.$ul.appendChild(newNode);
        }
    }

    init() {
        this.$elem.innerHTML = `
            <h2>토너먼트 목록</h2>
            <ul></ul>
            <button>방 만들기</button>
        `;

        this.$ul = this.$elem.querySelector("ul");
        this.$btn = this.$elem.querySelector("button");

        this.startInterval(3000, async () => {
            try {
                await tourListInfo.requestAPI();
                this.renderList(tourListInfo.recvData);
            }
            catch (e) {
                // to be modified
                alert(`Tournament List: ${e.message}`);
                this.requestShift("main_page");
            }
        });

        this.$btn.addEventListener("click", () => {
            this.requestShift("tour_make_room_subpage");
        });
    }

    fini() {
        clearInterval(this.interval);
        this.$elem.innerHTML = ``;
    }
};