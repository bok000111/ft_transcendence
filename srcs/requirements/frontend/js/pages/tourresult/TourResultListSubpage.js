import SubPage from "../SubPage.js"
import { tourResultPage } from "./TourResultPage.js"
import { tourResultListAPI } from "../../models/API.js"

class TourResultListSubpage extends SubPage {
    $tourList;

    async init() {
        this.$elem.innerHTML = `
          <h2 class="text-center">Tournament Result</h2>
          <div class="accordion accordion-flush" id="tour_list">
          </div>
        `;

        this.$tourList = this.$elem.querySelector("#tour_list");
        try {
            await tourResultListAPI.request();
            for (let i = 0; i < tourResultListAPI.recvData.data.results.length; i++) {
                let accordionItem = document.createElement("div");
                accordionItem.className = "accordion-item";
                accordionItem.innerHTML = `
                    <h2 class="accordion-header" id="flush-heading${i}">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapse${i}" aria-expanded="false" aria-controls="flush-collapse${i}">
                            ${tourResultListAPI.recvData.data.results[i].timestamp}
                        </button>
                    </h2>
                    <div id="flush-collapse${i}" class="accordion-collapse collapse" aria-labelledby="flush-heading${i}" data-bs-parent="#list_example">
                        <div class="accordion-body" id="detailTable-${i}"></div>
                    </div>`;
                let tableItem = this.$elem.querySelector(`#detailTable-${i}`);
                tableItem.innerHTML = `
                <table class="table">
                <thead>
                    <tr>
                    <th scope="col">VS</th>
                    <th scope="col">type</th>
                    <th scope="col">winner</th>
                    <th scope="col">score</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <th scope="row">${tourResultListAPI.recvData.data.results[i].sub_games[0].players[0]} vs ${tourResultListAPI.recvData.data.results[i].sub_games[0].players[1]}</th>
                    <td>${tourResultListAPI.recvData.data.results[i].sub_games[0].game_type}</td>
                    <td>${tourResultListAPI.recvData.data.results[i].sub_games[0].winner}</td>
                    <td>${tourResultListAPI.recvData.data.results[i].sub_games[0].score[0]} : ${tourResultListAPI.recvData.data.results[i].sub_games[0].score[1]}</td>
                    </tr>
                    <tr>
                    <th scope="row">${tourResultListAPI.recvData.data.results[i].sub_games[1].players[0]} vs ${tourResultListAPI.recvData.data.results[i].sub_games[1].players[1]}</th>
                    <td>${tourResultListAPI.recvData.data.results[i].sub_games[1].game_type}</td>
                    <td>${tourResultListAPI.recvData.data.results[i].sub_games[1].winner}</td>
                    <td>${tourResultListAPI.recvData.data.results[i].sub_games[1].score[0]} : ${tourResultListAPI.recvData.data.results[i].sub_games[1].score[1]}</td>
                    </tr>
                    <tr>
                    <th scope="row">${tourResultListAPI.recvData.data.results[i].sub_games[2].players[0]} vs ${tourResultListAPI.recvData.data.results[i].sub_games[2].players[1]}</th>
                    <td>${tourResultListAPI.recvData.data.results[i].sub_games[2].game_type}</td>
                    <td>${tourResultListAPI.recvData.data.results[i].sub_games[2].winner}</td>
                    <td>${tourResultListAPI.recvData.data.results[i].sub_games[2].score[0]} : ${tourResultListAPI.recvData.data.results[i].sub_games[2].score[1]}</td>
                    </tr>
                </tbody>
                </table>`;
                this.$tourList.appendChild(accordionItem);
            }
        }
        catch {
            alert("Failed to load Tournament Result...");
            this.route("main_page/main_subpage");
        }
    }

    fini() {
        this.$elem.innerHTML = ``;
    }
}

export const resultListSubpage = new TourResultListSubpage(
    tourResultPage.$elem.querySelector("div"),
    tourResultPage,
    null,
    "tour_result_list_subpage",
)