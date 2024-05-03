import Page from "./Page.js";
import { tourListInfo, tourRoomInfo } from "./Info.js";

class TourListPage extends Page{
    interval;

    setup() {
        this.mount("tour_room_page");
    }

    setEvent() {
        this.$elem.querySelector("button").addEventListener("click", () => {
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
                tourRoomInfo.sendData.roomNum = elem.roonNum;
                this.shift("tour_room_page");
            });
            ul.appendChild(newNode);
        }
        this.$elem.appendChild(ul);
    }

    init() {
        this.startInterval(async () => {
            try {
                await tourListInfo.requestAPI();
                this.renderList(tourListInfo.data);
            }
            catch (e) {
                alert(`Tournament List: ${e.message}`);
            }
        }, 3000);
    }

    fini() {
        clearInterval(interval);
        this.$elem.lastChild.remove();
    }
};