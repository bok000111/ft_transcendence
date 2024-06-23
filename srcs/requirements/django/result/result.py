from datetime import datetime
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()


class SubGame:
    def __init__(self, players, game_id, game_type, score):
        self.players = players
        self.game_id = game_id
        self.game_type = game_type
        self.score = score
        self.winner = self.determine_winner()

    def determine_winner(self):
        if self.score[0] > self.score[1]:
            return self.players[0]
        else:
            return self.players[1]

    def to_dict(self):
        return {
            "players": self.players,
            "game_type": self.game_type,
            "winner": self.winner,
            "score": self.score,
        }

    def __str__(self):
        return f"Players: {self.players}, Game Type: {self.game_type}, Score: {self.score}, Winner: {self.winner}"


class TournamentResult:
    def __init__(self, raw_data):
        split_data = raw_data.split(",")
        self.__parse(split_data)
        self.sub_games.sort(key=lambda x: x.game_id)

    # @classmethod
    # async def create(cls, raw_data):
    #     result = cls()
    #     split_data = raw_data.split(",")
    #     await result.__parse(split_data)
    #     result.sub_games.sort(key=lambda x: x.game_id)
    #     return result

    def __user_id_to_username(self, user_id):
        # return await sync_to_async(User.objects.get)(id=user_id).username
        # return sync_to_async(User.objects.get(id=user_id).username)()
        return User.objects.get(pk=user_id).username

    def __parse(self, split_data):
        self.timestamp = datetime.fromtimestamp(int(split_data[0]))
        players = [self.__user_id_to_username(pk) for pk in split_data[1:5]]
        # players = [int(id) for id in split_data[1:5]]

        sub_games_data = split_data[5:]
        self.sub_games = []
        for i in range(0, len(sub_games_data), 3):
            game_id = int(sub_games_data[i])
            score = [int(sub_games_data[i + 1]), int(sub_games_data[i + 2])]
            if game_id == 2:
                sub_players = players[:2]  # player1, player2
                game_type = "semi_final"
            elif game_id == 3:
                sub_players = players[2:]  # player3, player4
                game_type = "semi_final"
            elif game_id == 1:
                # ID가 1인 게임은 나중에 승자가 결정된 후 처리
                continue
            sub_game = SubGame(sub_players, game_id, game_type, score)
            self.sub_games.append(sub_game)

        final_game_data = sub_games_data[:3]
        final_game_id = int(final_game_data[0])
        final_score = [int(final_game_data[1]), int(final_game_data[2])]
        semi_final_winners = [self.sub_games[0].winner, self.sub_games[1].winner]
        final_game = SubGame(semi_final_winners, final_game_id, "final", final_score)
        self.sub_games.append(final_game)

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "sub_games": [game.to_dict() for game in self.sub_games],
        }

    def __str__(self):
        return f"Timestamp: {self.timestamp}, Sub Games[0]: {self.sub_games[0]}, Sub Games[1]: {self.sub_games[1]}, Sub Games[2]: {self.sub_games[2]}"

    def __repr__(self):
        return f"Timestamp: {self.timestamp}, Sub Games: {self.sub_games}"
