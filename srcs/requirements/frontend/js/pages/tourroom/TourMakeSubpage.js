import SubPage from "../SubPage.js";
import { tourMakeInfo, tourRoomInfo } from "../../models/Info.js";

class TourMakeSubpage extends SubPage {
    $form;
    $btn;

    init() {
        this.$elem.innerHTML = `
            <h2>방 생성</h2>
            <form>
                <input id="room-name" type="text" placeholder="room-name">
                <input id="nickname" type="text" placeholder="nickname">
                <input type="submit" value="생성"
            </form>
            <button>뒤로 가기</button>
        `;

        this.$form = this.$elem.querySelector("form");
        this.$btn = this.$elem.querySelector("button");

        this.$form.addEventListener("submit", async (event) => {
            event.preventDefault();
            tourMakeInfo.sendData[roomName] = this.$form.querySelector("#room-name").value;
            tourMakeInfo.sendData[nickname] = this.$form.querySelector("#nickname").value;
            try {
                await tourRoomInfo.requestAPI();
                tourRoomInfo.sendData[roomID] = tourMakeInfo.recvData[roomID];
                tourRoomInfo.sendData[nickname] = tourMakeInfo.recvData[nickname];
                this.requestShift("tour_room_subpage");
            }
            catch (e) {
                alert(`Tournament Make Room: ${e.message}`);
                this.$form.querySelector("#room-name").value = "";
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