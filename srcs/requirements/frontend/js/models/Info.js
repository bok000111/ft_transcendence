class Info {
    sendData = {};
    recvData = {};
    // API 전송 / 수신하는 함수
    requestAPI;

    constructor(requestAPI) {
        this.requestAPI = requestAPI.bind(this.sendData, this.recvData);
    }
};

/**
 * sendData = { email, password }
 * recvData = {}
 */
export const loginInfo = new Info(
    async (sendData, recvData) => {
        const response = await fetch("http://localhost:8000/api/login/", {
            method: "POST",
            headers: {
                "Host": "localhost:8000",
                "Origin": "http://localhost:5500",
                "Access-Control-Allow-Origin": "http://localhost:5500",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(sendData),
            credentials: "include",
        });
        if (!response.ok)
            throw new Error("HTTP Error");
        recvData = await JSON.parse(response);
        if (!response.success)
            throw new Error("Input Error");
        else
            return recvData;
    }
);

/**
 * sendData = { email, password, username }
 * recvData = {}
 */
export const signupInfo = new Info(
    async (sendData, recvData) => {
        const response = await fetch("http://localhost:8000/api/signup/", {
            method: "POST",
            headers: {
                "Host": "localhost:8000",
                "Origin": "http://localhost:5500",
                "Access-Control-Allow-Origin": "http://localhost:5500",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(sendData),
            credentials: "include",
        });
        if (!response.ok)
            throw new Error("HTTP Error");
        recvData = await JSON.parse(response);
        if (!response.success)
            throw new Error("Input Error");
        else
            return recvData;
    }
);

/**
 * POST
 * /api/logout/
 * sendData = {} // 5.17 명세 기준 전송 데이터 X
 * recvData = { message } // 성공 메시지
 *
*/
export const logoutInfo = new Info()(
    async (sendData, recvData) => {
        const response = await(fetch("http://localhost::8000/api/logout/"), {
            method: "POST",
            headers: {
                "Host": "localhost:8000",
                "Origin": "http://localhost:5500",
                "Access-Control-Allow-Origin": "http://localhost:5500",
                "Content-Type": "applicatoin/json",
            },
            body: JSON.stringify(sendData),
            credentials: "include",
        });
        if (!response.ok)
            throw new Error("HTTP Error");
        recvData = await JSON.parse(response);
        if (!response.message)
            throw new Error("Logout Error");
        else
            return recvData;
    }
);

/**
 * GET
 * /api/lobby/
 * sendData = {}
 * recvData = { statusCode, message, { lobbyID, lobbyName, curNum, maxNum }}
*/
export const tourListInfo = new Info();

/**
 * POST
 * /api/lobby/lobbyID/
 * sendData = { nickname }
 * recvData = { statusCode, message, {}}
*/
export const tourEntryInfo = new Info();

/**
 * POST
 * /api/lobby/
 * sendData = { lobbyName, nickname }
 * recvData = { statusCode, message, { lobbyID } }
 */
export const tourMakeInfo = new Info();

/**
 * GET
 * /api/lobby/lobbyID/
 * sendData = {}
 * recvData = { statusCode, message, lobbyID, lobbyName, players(자료구조 논의 필요) }
 */
export const tourRoomInfo = new Info();

/**
 * GET
 * /api/lobby/lobbyID/
 * sendData = {}
 * recvData = { statusCode, message, bracket(내부 구조: {번호(1 ~ 7), nickname(아직 안 한 경우 null), status(win, lose)}) }
 */
export const tourGameLoungeInfo = new Info();

/**
 * GET
 * PATH 미정  (5.18 기준)
 * sendData = {} // 일단은 없을듯?
 * recvData = { date, time, tourID }
*/
export const resultListInfo = new Info();

/**
 * sendData = { tourID }
 * recvData = { [ "playerID" : "rank" ] -> 이건 일단 위에서 받아놨던걸로 알아서 처리할 예정. + resultDetailInfo 삭제예정 }
 */
export const resultDetailInfo = new Info();