from bot_texts import BotTexts

WRITING = "WRITING"
DRAWING = "DRAWING"


class PicturePhoneGameLogic:

    def __init__(self, players=None):
        self.players = players
        self.finished = False
        self.current_phase = self._starting_phase()
        self.moves = PicturePhoneGameResults()
        self.MIN_PLAYERS = 4

    def next_player(self):
        if self.players:
            return self.players[0]
        else:
            raise PicturePhoneGameError("This game doesn't have players yet.")

    def play_turn(self, player_making_move, submission):
        if self.finished:
            raise PicturePhoneGameError("Cannot play turn when game is already finished.")
        else:
            self._advance_phase()
            self.moves.add_move(player_making_move, submission)
            self.players = self.players[1:]
            if not self.players:
                self.finished = True

    def set_players(self, new_players):
        self.players = new_players

    def results(self):
        return self.moves

    ### PRIVATE ###

    def _starting_phase(self):
        return WRITING

    def _advance_phase(self):
        self.current_phase = self._next_phase(self.current_phase)

    def _next_phase(self, phase_to_get_successor_of):
        return DRAWING if phase_to_get_successor_of == WRITING else WRITING


class PicturePhoneGameError(RuntimeError):
    pass

class NotEnoughPlayersError(PicturePhoneGameError):
    pass

class PlayerAlreadyJoinedError(PicturePhoneGameError):
    pass


class PicturePhoneGameResults:

    def __init__(self):
        self.contents = []

    def add_move(self, player_making_move, submission):
        self.contents.append((player_making_move, submission))

    def players_in_order(self):
        return [move[0] for move in self.contents]

    def submissions_in_order(self):
        return [move[1] for move in self.contents]


class PicturePhoneGameState:

    def __init__(self, game_id=0, debug=False):
        self.players = set()
        self.game_logic = PicturePhoneGameLogic()
        self.game_id = game_id
        self.started = False
        self.debug = debug

    def join_player(self, joining_player):
        if not self._game_started():
            self._add_player(joining_player)
        else:
            raise PicturePhoneGameError("Cannot join game after it has started.")

    def start(self):
        if not self._game_started():
            if self._number_of_players() < self.game_logic.MIN_PLAYERS:
                raise NotEnoughPlayersError(
                    "Cannot start game until at least {} players have joined.".format(self.game_logic.MIN_PLAYERS)
                )
            self.game_logic.set_players(list(self.players))
            self.started = True
            return True
        else:
            raise PicturePhoneGameError("Game already started.")

    def get_next_player(self):
        return self.game_logic.next_player()

    ### PRIVATE ###

    def _game_started(self):
        return self.started

    def _add_player(self, joining_player):
        if not joining_player in self.players:
            self.players.add(joining_player)
        else:
            raise PlayerAlreadyJoinedError("Player {} is already in the game.".format(joining_player))

    def _number_of_players(self):
        return len(self.players)


class PicturePhoneGame:

    def __init__(self, game_id, debug):
        self.game = PicturePhoneGameState(debug=debug)
        self.game_id = game_id
        self.debug = debug

    def start(self, context):
        self.game.start()
        player_id = self.game.get_next_player()
        context.bot.send_message(
            chat_id=player_id,
            text="You're first! Write something for the next player to draw."
        )

    def join_user(self, joining_user_id, context):
        try:
            self.game.join_player(joining_user_id)
            if self.debug:
                print("Player {} joined game {}".format(joining_user_id, self.game_id))
            context.bot.send_message(
                chat_id=joining_user_id,
                text="You've joined game {}.".format(self.game_id)
            )
        except PicturePhoneGameError:
            context.bot.send_message(
                chat_id=joining_user_id,
                text=BotTexts.already_joined
            )

    def min_players(self):
        return self.game.game_logic.MIN_PLAYERS