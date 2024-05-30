import SubPage from "../SubPage.js";
import { tourListAPI } from "../../models/API.js";
import { info } from "../../models/Info.js";
import { tourLobbyPage } from "./TourLobbyPage.js";

class TourListSubpage extends SubPage {
    $lobbyList;
    $refreshBtn;
    $makeBtn;

    render({ data }) {
        this.$lobbyList.innerHTML = ``;

        for (lobby of data.lobbies) {
            if (lobby.player_count === lobby.max_players)
                continue;

            const newNode = document.createElement("li");

            newNode.innerHTML = `
                <h3>${lobby.name}</h3>
                <h3>${lobby.player_count}/${lobby.max_players}</h3>
            `;
            newNode.addEventListener("click", () => {
                // 클로저의 성질을 잘 몰라서 얘는 될 지 모르겠다..
                info.lobby.id = lobby.id;
                this.requestShift("tour_entry_subpage");
            });
            this.$lobbyList.appendChild(newNode);
        }
    }

    async refresh() {
        try {
            await tourListAPI.request();
            this.render(tourListAPI.recvData);
        }
        catch (e) {
            alert(`Tournament List: ${e.message}`);
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

        this.$refreshBtn.addEventListener("click", this.refresh);
        this.$makeBtn.addEventListener("click", () => {
            this.requestShift("tour_make_subpage");
        });

        this.refresh();
    }

    fini() {
        this.$elem.innerHTML = ``;
    }
};

export const tourListSubpage = new TourListSubpage(
    tourLobbyPage.$elem.querySelector("div"),
    tourLobbyPage,
    null,
    "tour_list_subpage"
);