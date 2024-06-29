export const MODE = {
    NORMAL_2: 0,
    NORMAL_4: 1,
    TOURNAMENT: 2,
    LOCAL: 3,
    SUB_GAME: 4,
    AI: 5,
}

class Info {
    /*   deprecated?   */
    myID;
    myUsername;
    /*******************/
    games = {
        myNickname: "",
        state: [], // { name: "nickname", lose: true or false }
        type: null,
        maxPlayers: null,
    };
    curGame = {
        /**
         * id: number (gameid)
         * type: NORMAL_2 = 0 | NORMAL_4 = 1 | TOURNAMENT = 2 | LOCAL = 3 | SUB_GAME = 4 | AI = 5 ?
         * users: [str]
         * end_score: number
         * play_time: number
         */
    };

    initState(users) {
        this.games.state = [];
        this.games.state.push({
            name: "dummy",
            lose: false,
        });
        for (let i = 0; i < 3; ++i) {
            this.games.state.push({
                name: "???",
                lose: false,
            });
        }
        users.forEach((elem) => {
            this.games.state.push({
                name: elem,
                lose: false,
            });
        });
    }

    changeState(winner) {
        for (let i = 1; i < 8; ++i) {
            console.dir(this.games);
            if (this.games.state[i].name === winner) {
                if (i % 2 === 0) {
                    this.games.state[i + 1].lose = true;
                }
                else {
                    this.games.state[i - 1].lose = true;
                }
                this.games.state[i / 2].name = winner;
                break;
            }
        }
    }
};

export const info = new Info();

// export const info = {
//     /*   deprecated?   */
//     myID: null,
//     myUsername: null,
//     /*******************/
//     games: {
//         state: [],
//         type: null,
//         maxPlayers: null,
//     },
//     curGame: {
//         id: null,
//         type: null,
//         users: [],
//         end_score: null,
//         play_time: null,
//     },
// };