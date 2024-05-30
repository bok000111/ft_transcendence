import SubPage from "../SubPage.js";
import { normalListAPI } from "../../models/API.js";
import { info } from "../../models/Info.js";
import { normalLobbyPage } from "./NormalLobbyPage.js";

class NormalListSubpage extends SubPage {
    $lobbyList;
    $refreshBtn;
    $makeBtn;

    render({ data }) {
        this.$lobbyList.innerHTML = ``;

        for (let lobby of data.lobbies) {
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
                this.requestShift("normal_entry_subpage");
            });
            this.$lobbyList.appendChild(newNode);
        }
    }

    async refresh() {
        try {
            await normalListAPI.request();
            this.render(normalListAPI.recvData);
        }
        catch (e) {
            alert(`Normal List: ${e.message}`);
        }
    }

    init() {
        this.$elem.innerHTML = `
            <h2>게임 목록</h2>
            <button id="refresh">새로고침</button>
            <ul></ul>
            <button id="make">게임 만들기</button>
        `;

        this.$lobbyList = this.$elem.querySelector("ul");
        this.$refreshBtn = this.$elem.querySelector("#refresh");
        this.$makeBtn = this.$elem.querySelector("#make");

        this.$refreshBtn.addEventListener("click", () => {
            this.refresh();
        });
        this.$makeBtn.addEventListener("click", () => {
            this.requestShift("normal_make_subpage");
        });

        this.refresh();
    }

    fini() {
        this.$elem.innerHTML = ``;
    }
};

export const normalListSubpage = new NormalListSubpage(
    normalLobbyPage.$elem.querySelector("div"),
    normalLobbyPage,
    null,
    "normal_list_subpage"
);