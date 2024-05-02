import Info from "./Info.js";

export default signupInfo = new Info(
    async (obj, data) => {
        const response = await fetch("http://localhost:8000/api/signup/", {
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