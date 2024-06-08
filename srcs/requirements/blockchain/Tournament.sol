// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract TournamentManager {
    
    uint8 private constant SUB_GAME_COUNT = 3;
    uint8 private constant TUPLE_INFO = 5; // (game_id, player1, player2, score1, score2)
    uint8 private constant PLAYER_COUNT = 4;

    struct SubGame {
        uint64 game_id;
        uint64 player1;
        uint64 player2;
        uint8 score1;
        uint8 score2;
    }

    struct Tournament {
        uint timestamp;
        uint64[PLAYER_COUNT] players;
        SubGame[] sub_games;
    }

    mapping(uint64 => Tournament) private tournaments;
    uint64[] private valid_tournaments;

    function add_game(uint64 id, uint timestamp, uint64[PLAYER_COUNT] calldata players) external {
        tournaments[id] = Tournament(timestamp, players, new SubGame[](0));
    }

    function add_sub_game(uint64 id, uint64[TUPLE_INFO] calldata sub_game) external {
        require(tournaments[id].sub_games.length < SUB_GAME_COUNT, "SubGame count exceeded.");
        
        tournaments[id].sub_games.push(
            SubGame({
                game_id: sub_game[0],
                player1: sub_game[1],
                player2: sub_game[2],
                score1: uint8(sub_game[3]),
                score2: uint8(sub_game[4])
            })
        );

        // SUB_GAME_COUNT에 도달하면 is_valid를 true로 설정
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

    function get_tournament(uint64 id) external view returns (
        uint, 
        uint64, uint8, uint8, 
        uint64, uint8, uint8,
        uint64, uint8, uint8
    ) {
        Tournament storage tournament = tournaments[id];

        (uint64 game_id1, uint8 score1_1, uint8 score2_1) = get_subgame_info(tournament, 0);
        (uint64 game_id2, uint8 score1_2, uint8 score2_2) = get_subgame_info(tournament, 1);
        (uint64 game_id3, uint8 score1_3, uint8 score2_3) = get_subgame_info(tournament, 2);

        return (
            tournament.timestamp, 
            game_id1, score1_1, score2_1, 
            game_id2, score1_2, score2_2, 
            game_id3, score1_3, score2_3
        );
    }
}
