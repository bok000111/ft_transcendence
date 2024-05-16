import SubPage from "../SubPage.js";
import { tourRoomInfo } from "../../models/Info.js";

class TourRoomSubpage extends SubPage {
    interval;
    $title;
    $ol;
    $btn;

    startInterval(time, callback) {
        callback();
        this.interval = setInterval(callback, time);
    }

    init() {
        this.$elem.innerHTML = `
            <h2></h2>
            <ol></ol>
            <button>토너먼트 나가기</button>
        `;

        this.interval = null;
        this.$title = this.$elem.querySelector("h2");
        this.$ol = this.$elem.querySelector("ol");
        this.$btn = this.$elem.querySelector("button");

        this.startInterval(3000, async () => {
            try {
                await tourRoomInfo.requestAPI();
                /**
                 * 만약 현재 player의 status가 playing 상태로 바뀐다면,
                 * this.requestShift("pong_page"); 를 호출한다.
                 * 
                 * 그렇지 않다면, 현재 방의 정보와 대기 인원을 표시한다.
                 * 이 부분은 자료를 어떤 식으로 받을 것인지 선 논의 필요..
                 */
            }
            catch (e) {
                alert(`Tournament Room: ${e.message}`);
            }
        });

        this.$btn.addEventListener("click", () => {
            this.requestShift("tour_list_subpage");
        });
    }

    fini() {
        if (this.interval) {
            clearInterval(this.interval);
        }
        this.$elem.innerHTML = ``;
    }
};