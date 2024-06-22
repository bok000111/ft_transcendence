// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract TournamentContract {
    
    uint8 private constant SUB_GAME_COUNT = 3;
    uint8 private constant TUPLE_INFO = 3; // (game_id, player1, player2, score1, score2)
    uint8 private constant PLAYER_COUNT = 4;

    struct SubGame {
        uint8 game_id;
        uint8 score1;
        uint8 score2;
    }

    struct Tournament {
        uint64 timestamp;
        uint64[PLAYER_COUNT] players;
        SubGame[] sub_games;
    }

    mapping(uint64 => Tournament) private tournaments;
    uint64[] private valid_tournaments;

    function add_game(uint64 id, uint64 timestamp, uint64[PLAYER_COUNT] calldata players) external {
        Tournament storage tournament = tournaments[id];
        tournament.timestamp = timestamp;
        for (uint i = 0; i < players.length; i++)
            tournament.players[i] = players[i];
    }


    function add_sub_game(uint64 id, uint8[TUPLE_INFO] calldata sub_game) external {
        require(tournaments[id].sub_games.length < SUB_GAME_COUNT, "SubGame count exceeded.");
        
        tournaments[id].sub_games.push(
            SubGame({
                game_id: sub_game[0],
                score1: sub_game[1],
                score2: sub_game[2]
            })
        );

        // SUB_GAME_COUNT에 도달하면 valid_tournaments에 추가
        if(tournaments[id].sub_games.length == SUB_GAME_COUNT) {
            valid_tournaments.push(id);
        }
    }

    function get_valid_tournaments() external view returns (uint64[] memory) {
        return valid_tournaments;
    }

    function get_subgame_info(Tournament storage tournament, uint index) private view returns (uint64, uint8, uint8) {
        SubGame storage sub_game = tournament.sub_games[index];
        return (sub_game.game_id, sub_game.score1, sub_game.score2);
    }

    function uint_to_string(uint64 num) internal pure returns (string memory) {
        if (num == 0) {
            return "0";
        }

        uint64 len = 0;
        uint64 temp = num;
        while (temp > 0) {
            temp /= 10;
            len++;
        }

        bytes memory str = new bytes(len);
        while (num > 0) {
            str[--len] = bytes1(uint8(48 + num % 10));
            num /= 10;
        }

        return string(str);
    }

    function get_tournament(uint64 id) external view returns (string memory) {
        Tournament storage tournament = tournaments[id];

        (uint64 game_id1, uint8 score1_1, uint8 score2_1) = get_subgame_info(tournament, 0);
        (uint64 game_id2, uint8 score1_2, uint8 score2_2) = get_subgame_info(tournament, 1);
        (uint64 game_id3, uint8 score1_3, uint8 score2_3) = get_subgame_info(tournament, 2);

        return string(abi.encodePacked(
            uint_to_string(tournament.timestamp), ",",
            uint_to_string(tournament.players[0]), ",", uint_to_string(tournament.players[1]), ",",
            uint_to_string(tournament.players[2]), ",", uint_to_string(tournament.players[3]), ",",
            uint_to_string(game_id1), ",", uint_to_string(score1_1), ",", uint_to_string(score2_1), ",",
            uint_to_string(game_id2), ",", uint_to_string(score1_2), ",", uint_to_string(score2_2), ",",
            uint_to_string(game_id3), ",", uint_to_string(score1_3), ",", uint_to_string(score2_3)
        ));
    }

    function test_start(uint64 id) external view returns (string memory) {
        Tournament storage tournament = tournaments[id];

        return string(abi.encodePacked(
            uint_to_string(tournament.timestamp), ",",
            uint_to_string(tournament.players[0]), ",", uint_to_string(tournament.players[1]), ",",
            uint_to_string(tournament.players[2]), ",", uint_to_string(tournament.players[3])
        ));
    }

    function test_sub(uint64 id) external view returns (string memory) {
        Tournament storage tournament = tournaments[id];

        return string(abi.encodePacked(
            uint_to_string(tournament.sub_games[0].game_id), ",",
            uint_to_string(tournament.sub_games[0].score1), ",",
            uint_to_string(tournament.sub_games[0].score2)
        ));
    }
}
