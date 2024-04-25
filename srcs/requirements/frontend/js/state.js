const state = {
    login: true,
    menu: [
        "head",
        "tournament_register",
        "tournament_result",
        "game_start"
    ],
    tournament_room: {
        nickname: true,
        list: [
            {
                title: "님만 오면 고",
                num: 1
            },
            {
                title: "남만 오면 고",
                num: 2
            },
            {
                title: "남만의 왕 맹획",
                num: 3
            }
        ],
        room: [
            "jbok",
            "jdoh"
        ]
    },
    tournament_result: {
        list: [
            "2024/04/25 09:29:00",
            "2024/04/26 09:29:00",
            "2024/04/27 09:29:00"
        ],
        ranking: [
            "jbok",
            "changhyl",
            "mingkang",
            "sunwsong",
            "jdoh"
        ]
    },
    game: {
        /**
         * ...
         * 여기는 좀 더 생각해 봐야 함.
         * ball의 posX, posY,
         * paddle의 posX, posY에 대한 정보들을 포함시킬 것인가?
         * 현재 점수에 대한 정보를 포함시킬 것인가?
         */
    }
}