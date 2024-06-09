from datetime import datetime


class SubGame:
    def __init__(self, players, game_id, game_type, score):
        self.players = players
        self.game_id = game_id
        self.game_type = game_type
        self.score = score
        self.winner_id = self.determine_winner()

    def determine_winner(self):
        if self.score[0] > self.score[1]:
            return self.players[0]
        else:
            return self.players[1]

    def to_dict(self):
        return {
            'players': self.players,
            'game_id': self.game_id,
            'game_type': self.game_type,
            'score': self.score,
            'winner_id': self.winner_id
        }

    def __str__(self):
        return f"Players: {self.players}, Game Type: {self.game_type}, Score: {self.score}, Winner: {self.winner_id}"


class TournamentResult:
    def __init__(self, raw_data):
        split_data = raw_data.split(',')
        self.__parse(split_data)
        self.sub_games.sort(key=lambda x: x.game_id)

    def __parse(self, split_data):
        self.timestamp = datetime.fromtimestamp(int(split_data[0]))
        player_ids = [int(id) for id in split_data[1:5]]

        sub_games_data = split_data[5:]
        self.sub_games = []
        for i in range(0, len(sub_games_data), 3):
            game_id = int(sub_games_data[i])
            score = [int(sub_games_data[i+1]), int(sub_games_data[i+2])]
            if game_id == 2:
                players = player_ids[:2]  # player1, player2
                game_type = 'semi_final'
            elif game_id == 3:
                players = player_ids[2:]  # player3, player4
                game_type = 'semi_final'
            elif game_id == 1:
                # ID가 1인 게임은 나중에 승자가 결정된 후 처리
                continue
            sub_game = SubGame(players, game_id, game_type, score)
            self.sub_games.append(sub_game)

        final_game_data = sub_games_data[:3]
        final_game_id = int(final_game_data[0])
        final_score = [int(final_game_data[1]), int(final_game_data[2])]
        semi_final_winners = [
            self.sub_games[0].winner_id, self.sub_games[1].winner_id]
        final_game = SubGame(semi_final_winners,
                             final_game_id, 'final', final_score)
        self.sub_games.append(final_game)

    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'sub_games': [game.to_dict() for game in self.sub_games]
        }

    def __str__(self):
        return f"Timestamp: {self.timestamp}, Sub Games[0]: {self.sub_games[0]}, Sub Games[1]: {self.sub_games[1]}, Sub Games[2]: {self.sub_games[2]}"

    def __repr__(self):
        return f"Timestamp: {self.timestamp}, Sub Games: {self.sub_games}"
