// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Tournament {

    uint8 private constant ROUND_COUNT = 3;

    struct Player {
        uint64 id;
        string username;
        string nickname;
    }

    struct Round {
        Player[2] players;
        string round_type;
        uint64 winner_id;
        uint8[2] score;
    }

    Round[ROUND_COUNT] private rounds;
    uint8 private finished_round = 0;

    mapping(uint64 => Player) private players;

    function addPlayer(uint64 _id, string calldata _username, string calldata _nickname) external {
        players[_id] = Player(_id, _username, _nickname);
    }

    function saveResult() private {
        // round의 형식에 맞추어 result를 저장
    }

    function setWinner(uint8 round, uint8[2] calldata score) external returns(uint64) {
        rounds[round].score = score;
        finished_round += 1;

        if (finished_round == ROUND_COUNT)
            saveResult();
        
        return 1;
    }

    function setFinishedRound(uint8 _finished_round) external returns(uint64){
        finished_round = _finished_round;
        return finished_round;
    }

}