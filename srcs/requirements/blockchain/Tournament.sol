// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract Tournament {

    uint8 private constant ROUND_COUNT = 3;

    struct Player {
        uint64 id;
        string username;
        string nickname;
    }

    struct Round {
        uint8[2] score;
    }

    Round[ROUND_COUNT] private rounds;
    uint8 private finished_round = 0;

    mapping(uint64 => Player) private players;

    function addPlayer(uint64 _id, string memory _username, string memory _nickname) external {
        players[_id] = Player(_id, _username, _nickname);
    }

    function saveResult() private {
        finished_round = 0;
        
    }

    function setWinner(uint8 round, uint8[2] memory score) external {
        rounds[round].score = score;
        finished_round += 1;

        if (finished_round == ROUND_COUNT)
            saveResult();
    }


}