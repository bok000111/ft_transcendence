import Info from "./Info.js";

/**
 * (로그인과 관련하여)
 * 어떤 정보를 백에서 받아오는가?
 * 어떤 정보를 백으로 보내는가?
 * 에 대한 논의 필요
 */

export default loginInfo = new Info(
    async (obj, data) => {
        const response = await fetch("http://localhost:8000/api/login/", {
            method: "POST",
            headers: {
                "Host": "localhost:8000",
                "Origin": "http://localhost:5500",
                "Access-Control-Allow-Origin": "http://localhost:5500",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
            credentials: "include",
        });
        if (!response.ok)
            throw new Error("HTTP Error");
        obj.data = await response.json();
        if (!response.success)
            throw new Error("Input Error");
        else
            return obj.data;
    }
);