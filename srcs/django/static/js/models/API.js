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
export const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
console.log(`csrftoken: ${csrftoken}`);
export const BASE_HOST = "localhost";
export const BASE_URL = "https://localhost:4242/";
export const BASE_WS_URL = "wss://localhost:4242/ws/";

class API {
    uri;
    method;
    sendData = {};
    recvData = {};

    constructor(uri, method) {
        this.uri = uri;
        this.method = method;
    }

    async request() {
        const httpRequest = {
            method: this.method,
            headers: {
                "Host": BASE_HOST,
                "Origin": BASE_URL,
                "Access-Control-Allow-Origin": BASE_URL,
                "X-CSRFToken": csrftoken,
            },
            // mode: "same-origin",
            credentials: "include",
        }
        if (this.method === "POST") {
            httpRequest.body = JSON.stringify(this.sendData);
            httpRequest.headers["Content-Type"] = "application/json";
        }
        const response = await fetch(this.uri, httpRequest);
        this.recvData = await response.json();
        if (!response.ok) {
            throw new Error(this.recvData.message);
        }
    }
};

/**
 * sendData = { email, password }
 * recvData = {}
 */
export const loginAPI = new API(
    `${BASE_URL}api/user/login/`,
    "POST"
);

/**
 * sendData = { email, password, username }
 * recvData = {}
 */
export const signupAPI = new API(
    `${BASE_URL}api/user/signup/`,
    "POST"
);

/**
 * POST
 * /api/logout/
 * sendData = {} // 5.17 명세 기준 전송 데이터 X
 * recvData = { message } // 성공 메시지
 *
*/
export const logoutAPI = new API(
    `${BASE_URL}api/user/logout/`,
    "POST"
);

export const meAPI = new API(
    `${BASE_URL}api/user/me/`,
    "GET"
);

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
 * recvData = { resultData: [id, date, tourResult{}] }
 * tourResult -> {
 * player1 nickname: String
 * player2 nickname: String
 * player1 score: Int
 * player2 score: Int
 * }
*/
export const tourResultListAPI = new API(
    `${BASE_URL}api/result/`,
    "GET"
);