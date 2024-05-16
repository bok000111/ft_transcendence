import SubPage from "../SubPage.js";
import { tourEntryInfo, tourRoomInfo } from "../../models/Info.js";

class TourEntrySubpage extends SubPage {
    $form;
    $btn;

    init() {
        this.$elem.innerHTML = `
            <h2>닉네임 입력</h2>
            <form>
                <input id="nickname" type="text" placeholder="nickname">
                <input type="submit" value="입력">
            </form>
            <button>뒤로 가기</button>
        `;

        this.$form = this.$elem.querySelector("form");
        this.$btn = this.$elem.querySelector("button");

        this.$form.addEventListener("submit", async (event) => {
            event.preventDefault();
            tourEntryInfo.sendData[nickname] = this.$form.querySelector("#nickname").value;
            try {
                await tourEntryInfo.requestAPI();
                // 받은 데이터에서 roomID, nickname에 해당하는 내용을 tourRoomInfo에 미리 저장해 놓는다.
                // 나중에 TourRoom에서 API를 보낼 때 이 때 저장된 정보를 바탕으로 전송한다.
                tourRoomInfo.sendData[roomID] = tourEntryInfo.recvData[roomID];
                tourRoomInfo.sendData[nickname] = tourEntryInfo.recvData[nickname];
                this.requestShift("tour_room_subpage");
            }
            catch (e) {
                alert(`Tournament Entry: ${e.message}`);
                this.$form.querySelector("#nickname").value = "";
            }
        });

        this.$btn.addEventListener("click", () => {
            this.requestShift("tour_list_subpage");
        });
    }

    fini() {
        this.$elem.innerHTML = ``;
    }
};