import SubPage from "../SubPage.js";
import { tourRoomInfo } from "../../models/Info.js";

class TourEntrySubpage extends SubPage {
    $form;
    $btn;

    init() {
        this.$elem.innerHTML = `
            <form>
                <input id="nickname" type="text" placeholder="nickname">
                <input type="submit" value="enter">
            </form>
            <button>뒤로 가기</button>
        `;

        this.$form = this.$elem.querySelector("form");
        this.$btn = this.$elem.querySelector("button");

        this.$form.addEventListener("submit", async (event) => {
            event.preventDefault();
            tourRoomInfo.sendData[nickname] = this.$form.querySelector("#nickname").value;
            try {
                await tourRoomInfo.requestAPI();
                this.requestShift("tour_room_subpage");
            }
            catch (e) {

            }
        });

        this.$btn.addEventListener("click", () => {
            this.requestShift("tour_list_subpage");
        });
    }

    fini() {

    }
};