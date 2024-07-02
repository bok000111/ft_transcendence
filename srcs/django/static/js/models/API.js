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

let csrftoken = null;

export const updateAccessToken = (token) => {
    if (token === null || token === undefined) {
        window.localStorage.removeItem("access_token");
        return;
    }
    window.localStorage.setItem("access_token", token);
    console.log(`access_token: ${token}`);
};

export const BASE_HOST = "localhost";
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
        let access_token = window.localStorage.getItem("access_token");
        let http_body = null;
        let headers = { "X-CSRFToken": csrftoken, };

        if (access_token) {
            headers["Authorization"] = `Bearer ${access_token}`;
        }
        if (this.method === "POST" || this.method === "PUT") {
            http_body = JSON.stringify(this.sendData);
            headers["Content-Type"] = "application/json";
        }

        const httpRequest = {
            method: this.method,
            headers: headers,
            body: http_body,
            mode: "same-origin",
            credentials: "include",
        }

        const response = await fetch(this.uri, httpRequest);
        this.recvData = await response.json();
        if (!response.ok) {
            throw new Error(this.recvData.message);
        }
        if (this.recvData?.data?.access_token) {
            updateAccessToken(this.recvData.data.access_token);
        }
    }
};

/**
 * sendData = { email, password }
 * recvData = {}
 */
export const loginAPI = new API(
    "/api/user/login/",
    "POST"
);

/**
 * sendData = { email, password, username }
 * recvData = {}
 */
export const signupAPI = new API(
    "/api/user/signup/",
    "POST"
);

export const jwtAPI = new API(
    "/api/2fa/",
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
    "/api/user/logout/",
    "POST"
);

export const meAPI = new API(
    "/api/user/me/",
    "GET"
);

export const csrfTokenAPI = new API(
    "/api/user/csrf/",
    "GET"
);

if (csrftoken === null) {
    csrfTokenAPI.request().then(() => {
        csrftoken = csrfTokenAPI.recvData.data.csrftoken;
        console.log(`csrftoken: ${csrftoken}`);
    });
}
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
    "/api/result/",
    "GET"
);