/**
 * 기본 http 통신의 경우,
 * {
 *     status,
 *     message,
 *     data: {}
 * }
 * 요런 식으로 들어온다.
 * status code의 경우에는 http response의 status code로 들어온다. ( fail + error )
 */

class API {
    sendData = {};
    recvData = {};
    // API 전송 / 수신하는 함수
    request;

    constructor(request) {
        this.request = request.bind(this);
    }
};

/**
 * sendData = { email, password }
 * recvData = {}
 */
export const loginAPI = new API(
    async function() {
        const response = await fetch("http://localhost:8000/api/user/login/", {
            method: "POST",
            headers: {
                "Host": "localhost:8000",
                "Origin": "http://localhost:5500",
                "Access-Control-Allow-Origin": "http://localhost:5500",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(this.sendData),
            credentials: "include",
        });
        this.recvData = await response.json();
        if (!response.ok) {
            throw new Error(this.recvData.message);
        }
    }
);

/**
 * sendData = { email, password, username }
 * recvData = {}
 */
export const signupAPI = new API(
    async function() {
        const response = await fetch("http://localhost:8000/api/user/signup/", {
            method: "POST",
            headers: {
                "Host": "localhost:8000",
                "Origin": "http://localhost:5500",
                "Access-Control-Allow-Origin": "http://localhost:5500",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(this.sendData),
            credentials: "include",
        });
        this.recvData = await response.json();
        if (!response.ok) {
            throw new Error(this.recvData.message);
        }
    }
);

/**
 * POST
 * /api/logout/
 * sendData = {} // 5.17 명세 기준 전송 데이터 X
 * recvData = { message } // 성공 메시지
 *
*/
export const logoutAPI = new API(
    async function() {
        const response = await fetch("http://localhost:8000/api/user/logout/", {
            method: "POST",
            headers: {
                "Host": "localhost:8000",
                "Origin": "http://localhost:5500",
                "Access-Control-Allow-Origin": "http://localhost:5500",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(this.sendData),
            credentials: "include",
        });
        this.recvData = await response.json();
        if (!response.ok) {
            throw new Error(this.recvData.message);
        }
    }
);

// <*** TournamentLobby Object ***>
// TournamentLobby: {
// 	"id": number,
// 	"name": string,
// 	"players": PlayerInLobby[],
// 	"player_count": number,
// 	"max_players": number,
// 	"end_score": number,
// }

/**
 * GET
 * /api/tournament/
 * sendData = {}
 * recvData = { status, message, data: { "lobbies": TournamentLobby[] } } // TournamentLobby 구조체 추가 예정
*/
export const tourListAPI = new API(
    async function() {
        const response = await fetch("http://localhost:8000/api/tournament/", {
            method: "GET",
            headers: {
                "Host": "localhost:8000",
                "Origin": "http://localhost:5500",
                "Access-Control-Allow-Origin": "http://localhost:5500",
                // "Content-Type": "application/json",
            },
            // body: JSON.stringify(this.sendData),
            credentials: "include",
        });
        this.recvData = await response.json();
        if (!response.ok) {
            throw new Error(this.recvData.message);
        }
    }
);

/**
 * POST
 * /api/tournament/id/
 * sendData = { nickname }
 * recvData = { status, message, data: { "lobby": TournamentLobby }}
*/
export const tourEntryAPI = new API(
    async function() {
        const tournamentID = this.sendData.id;
        delete this.sendData.id;
        const response = await fetch(`http://localhost:8000/api/tournament/${tournamentID}/`, {
            method: "POST",
            headers: {
                "Host": "localhost:8000",
                "Origin": "http://localhost:5500",
                "Access-Control-Allow-Origin": "http://localhost:5500",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(this.sendData),
            credentials: "include",
        });
        this.recvData = await response.json();
        if (!response.ok) {
            throw new Error(this.recvData.message);
        }
    }
);

/**
 * POST
 * /api/tournament/
 * sendData = { name, nickname }
 * recvData = { status, message, data: { "lobby": TournamentLobby } }
 */
export const tourMakeAPI = new API(
    async function() {
        const response = await fetch(`http://localhost:8000/api/tournament/`, {
            method: "POST",
            headers: {
                "Host": "localhost:8000",
                "Origin": "http://localhost:5500",
                "Access-Control-Allow-Origin": "http://localhost:5500",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(this.sendData),
            credentials: "include",
        });
        this.recvData = await response.json();
        if (!response.ok) {
            throw new Error(this.recvData.message);
        }
    }
);

/**
 * GET
 * /api/tournament/id/
 * sendData = {}
 * recvData = { statusCode, message, data: { "lobby": TournamentLobby } }
 */
// export const tourLobbyInfo = new Info();

/**
 * <*** WebSocket ***>
 * /api/tournament/id/
 * sendData = {}
 * recvData = { statusCode, message, bracket(내부 구조: {번호(1 ~ 7), nickname(아직 안 한 경우 null), status(win, lose)}) }
 */
// export const tourGameLoungeInfo = new Info();

/** 미정 API
 * GET
 * PATH 미정  (5.18 기준)
 * sendData = {} // 일단은 없을듯?
 * recvData = { date, time, tourID }
*/
export const tourResultListAPI = new API(
    async function() {
        const response = await fetch(`http://localhost:8000/api/result/`, {
            method: "POST",
            headers: {
                "Host": "localhost:8000",
                "Origin": "http://localhost:5500",
                "Access-Control-Allow-Origin": "http://localhost:5500",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(this.sendData),
            credentials: "include",
        });
        this.recvData = await response.json();
        if (!response.ok) {
            throw new Error(this.recvData.message);
        }
    }
);

/** 미정 API
 * sendData = { tourID }
 * recvData = { [ "playerID" : "rank" ] -> 이건 일단 위에서 받아놨던걸로 알아서 처리할 예정. + resultDetailInfo 삭제예정 }
 */
export const tourResultDetailAPI = new API(
    async function() {
        const response = await fetch(`http://localhost:8000/api/tournament/`, {
            method: "POST",
            headers: {
                "Host": "localhost:8000",
                "Origin": "http://localhost:5500",
                "Access-Control-Allow-Origin": "http://localhost:5500",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(this.sendData),
            credentials: "include",
        });
        this.recvData = await response.json();
        if (!response.ok) {
            throw new Error(this.recvData.message);
        }
    }
);