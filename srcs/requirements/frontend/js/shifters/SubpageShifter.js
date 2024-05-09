import PageShifter from "./PageShifter.js";

export class SubpageShifter extends PageShifter {
    shift(nextPage) {
        this.$currentPage.fini(); // 지금꺼 종료
        this.$currentPage = this.pages[nextPage];
        this.$currentPage.init(); // 지금꺼 초기화
    }
};

export const login_shifter = new SubpageShifter("login_sub_page");
export const main_shifter = new SubpageShifter("main_sub_page");
export const tour_make_shifter = new SubpageShifter("tour_make_sub_page");
export const tour_res_shifter = new SubpageShifter("tour_res_sub_page");
export const match_shifter = new SubpageShifter("matchmaking_sub_page");
export const pong_shifter = new SubpageShifter("pong_sub_page");

/*
   ***  page  ***
1. login
    1.1. login
    1.2. signup
2. main page
    X
3. tournament making
    3.1. tournament list
    3.2. nickname entry
    3.3. tournament room
4. matchmaking -> 미정
    4.1. select playerNum
    4.2. matching...
5. tournament result
    5.1. result list
    5.2. result detail
6. pong (아직은 프로토타입)
    6.1. game
    6.2. pause
    6.3. ending of game
*/
