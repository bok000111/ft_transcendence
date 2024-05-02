export default class Info {
    data = {};
    // API 전송 / 수신하는 함수
    requestAPI;

    constructor(requestAPI) {
        this.requestAPI = requestAPI.bind(this);
    }
};

/**
 * 아마 위 클래스를 상속받아서 사용할 듯.
 * ex) class LoginInfo extends Info;
 * 
 * 상속받은 클래스를 proxy로 감싸거나,
 * 
 * 그냥 상속을 받지 말고 바로 proxy로 감싸서 써도 괜찮을 듯.
 * 논의 필요.
 * 
 * 사실 토너먼트의 경우에는 주기적으로 API 요청을 해야하기 때문에
 * 단순히 Info를 상속받는 것으로는 부족할 수 있다.
 * Page 클래스에서 처리하게 만들어도 괜찮을 듯.
 */

// async function receiveInfo(requestAPI) {
//     const data = await requestAPI();

//     render(data);
// }

// setInterval(receiveInfo, 1000);