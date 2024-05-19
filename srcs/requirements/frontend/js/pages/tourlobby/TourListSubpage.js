import SubPage from "../SubPage.js";
import { tourListInfo, tourEntryInfo } from "../../models/Info.js";

class TourListSubpage extends SubPage {
    $lobbyList;
    $refreshBtn;
    $makeBtn;

    renderList({ lobbies }) {
        this.$lobbyList.innerHTML = ``;

        for (lobby of lobbies) {
            if (lobby.player_count === lobby.max_players)
                continue;

            const newNode = document.createElement("li");

            newNode.innerHTML = `
                <h3>${lobby.name}</h3>
                <h3>${lobby.player_count}/${lobby.max_players}</h3>
            `;
            newNode.addEventListener("click", () => {
                // 클로저의 성질을 잘 몰라서 얘는 될 지 모르겠다..
                tourEntryInfo.sendData[id] = lobby.id;
                this.requestShift("tour_entry_subpage");
            });
            this.$lobbyList.appendChild(newNode);
        }
    }

    init() {
        this.$elem.innerHTML = `
            <h2>토너먼트 목록</h2>
            <button id="refresh">새로고침</button>
            <ul></ul>
            <button id="make">토너먼트 만들기</button>
        `;

        this.$lobbyList = this.$elem.querySelector("ul");
        this.$refreshBtn = this.$elem.querySelector("#refresh");
        this.$makeBtn = this.$elem.querySelector("#make");

        this.$refreshBtn.addEventListener("click", async () => {
            try {
                await tourListInfo.requestAPI();
                this.renderList(tourListInfo.recvData.data);
            }
            catch (e) {
                alert(`Tournament List: ${e.message}`);
            }
        });

        this.$makeBtn.addEventListener("click", this.requestShift("tour_make_subpage"));
    }

    fini() {
        this.$elem.innerHTML = ``;
    }
};