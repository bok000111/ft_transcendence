import Page from "./Page.js";
import Component from "./Component.js";

class MainPage extends Page {
    $logoutBtn;
    $participateBtn;
    $tournamentResultBtn;
    $matchmakingBtn;

    setup() {
        this.mount("main_page");
        this.$logoutBtn = this.$elem.querySelector("#logout");
        this.$participateBtn = this.$elem.querySelector("#participate");
        this.$tournamentResultBtn = this.$elem.querySelector("#tournamentResult");
        this.$matchmakingBtn = this.$elem.querySelector("#matchmaking");
    }

    setEvent() {
        // logout process 던져줘야함. 변경 가능성 있음.
        this.$logoutBtn.addEventListener("click", () => {
            postLogoutInfo = async (data) => {
                const response = await fetch("http://localhost:8000/api/logout/", {
                    method: "POST",
                    headers: {
                        "Host": "localhost:8000",
                        "Origin": "http://localhost:5500",
                        "Access-Control-Allow-Origin": "http://localhost:5500",
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data),
                    credentials: "include"
                });
        
                if (!response.ok) {
                    alert("`HTTP Error : ${response.status}`");
                }
                else {
                    const res = await response.json();
                    if (res.success) {
                        this.shift("login_page");
                    }
                    else
                        alert("Logout Failed...");
                }
            };
        });

        this.$participateBtn.addEventListener("click", () => {
            this.shift("tour_room_page");
        });

        this.$tournamentResultBtn.addEventListener("click", () => {
            this.shift("tour_result_page");
        });

        this.$matchmakingBtn.addEventListener("click", () => {
            this.shift("match_making_page");
        });
    }
}
