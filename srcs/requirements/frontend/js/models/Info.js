class Info {
    sendData = {};
    recvData = {};
    // API 전송 / 수신하는 함수
    requestAPI;

    constructor(requestAPI) {
        this.requestAPI = requestAPI.bind(this.sendData, this.recvData);
    }
};

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
 * sendData = {}
 * recvData = { success, failureMsg, roomID, roomName, curNum, maxNum }
 */
export const tourListInfo = new Info();

/**
 * sendData = { roomID, nickname }
 * recvData = { success, failureMsg, roomID, nickname }
 */
export const tourEntryInfo = new Info();

/**
 * sendData = { roomName, nickname }
 * recvData = { success, failureMsg, roomID, nickname }
 */
export const tourMakeInfo = new Info();

/**
 * sendData = { roomID, nickname }
 * recvData = { success, failureMsg, roomID, roomName, players(자료구조 논의 필요) }
 */
export const tourRoomInfo = new Info();

/**
 * 아직 미완성.
 * sendData = { type: { one/two/three/four } }
 * recvData = { ... }
 */
export const matchMakingInfo = new Info();