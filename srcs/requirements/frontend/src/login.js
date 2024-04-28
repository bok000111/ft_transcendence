const $login = document.querySelector(".login-class");
const $signupBtn = document.querySelector("button");
const $signup = document.querySelector(".signup");
const $main = document.querySelector(".main");
$signupBtn.addEventListener("click", () => {
    $login.classList.add("none");
    $signupBtn.classList.add("none");
    $signup.classList.remove("none");
});

class Login {
    $loginForm;
    userId;

    constructor(login) {
        this.$loginForm = login;
        this.setEvent();
    }

    setEvent() {
        this.$loginForm.addEventListener("submit", (event) => {
            event.preventDefault();
            this.postLoginInfo({
                email: this.$loginForm.querySelector("input:first-child").value,
                password: this.$loginForm.querySelector("input:nth-child(2)").value
            });
        })
    }

    postLoginInfo = async (data) => {
        const response = await fetch("http://localhost:8000/api/login/", {
            method: "POST",
            headers: {
                "Host": "localhost:8000",
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            alert("`HTTP Error : ${response.status}`");
        }
        else {
            const res = await response.json();
            if (res.success) {
                this.inputId = res.data.username;
                this.$loginForm.classList.add("none");
                $main.classList.remove("none");
            }
            else
                alert("Wrong Id or Password!");
        }
    };
};

class Signup {
    $signup;

    constructor(signup) {
        this.$signup = signup;
        this.setEvent();
    }

    setEvent() {
        this.$signup.addEventListener("submit", (event) => {
            event.preventDefault();
            this.postSignupInfo({
                email: this.$signup.querySelector("input:first-child").value,
                password: this.$signup.querySelector("input:nth-child(2)").value,
                username: this.$signup.querySelector("input:nth-child(3)").value
            });
        });
    }

    // postSignupInfo = async (data) => {
    //     try {
    //         const response = await fetch("https://localhost:8000/api/signup/", {
    //             method: "POST", // POST 요청을 사용
    //             headers: {
    //                 "Content-Type": "application/json" // 요청 데이터가 JSON 형식임을 지정
    //             },
    //             body: JSON.stringify(data) // 객체를 JSON 문자열로 변환하여 전송
    //         });

    //         if (!response.ok) { // 응답이 정상적인지 확인
    //             throw new Error(`HTTP 오류: ${response.status}`); // 오류가 발생하면 예외를 발생시킴
    //         }

    //         const result = await response.json(); // 응답을 JSON으로 파싱

    //         if (result.status === "success") {
    //             alert("signup success");
    //             this.$signup.classList.add("none");
    //             $main.classList.remove("none");
    //             return true;
    //         }
    //         else {
    //             alert("signup failed");
    //             return false;
    //         }
    //     } catch (error) {
    //         alert("signup failed");
    //         return false;
    //     }
    // };
    postSignupInfo = async (data) => {
        const response = await fetch("http://localhost:8000/api/signup/", {
            method: "POST",
            headers: {
                "Host": "localhost:8000",
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            alert("`HTTP Error : ${response.status}`");
        }
        else {
            const res = await response.json();
            if (res.success) {
                this.$signup.classList.add("none");
                $main.classList.remove("none");
            }
            else
                alert("Wrong Id or Password!");
        }
    };
};

const login = new Login($login);
const signup = new Signup($signup);
