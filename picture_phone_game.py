from bot_texts import BotTexts
from game_errors import *

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

    def is_in_drawing_phase(self):
        return self.game_logic.current_phase == DRAWING

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

    def __init__(self, game_id, game_database, debug):
        self.game_state = PicturePhoneGameState(debug=debug)
        self.game_database = game_database
        self.game_id = game_id
        self.debug = debug

    def start(self, update, context):
        try:
            self.game_state.start()
            player_id = self.game_state.get_next_player()
            message = context.bot.send_message(
                chat_id=player_id,
                text="You're first! Reply to this message with a written prompt for the next player to draw."
            )
            self.game_database.put_game_for_message(message, self)
        except NotEnoughPlayersError:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You must wait until {} players have joined!".format(self.min_players())
            )

    def join_user(self, joining_user_id, context):
        try:
            self.game_state.join_player(joining_user_id)
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

    def play_turn(self, update, context):
        if self.game_state.is_in_drawing_phase():
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="simple simon, the ass man"
            )
        else:
            if update.message.text:
                # User submission is valid! Store it and advance to the next phase.
                self.game_database.put_game_for_message(update.message, self)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="YOU'RE CORRECT!"
                )
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Please try again with a description."
                )

    def min_players(self):
        return self.game_state.game_logic.MIN_PLAYERS


class GameDatabase:

    def __init__(self, debug=False):
        self.games_by_id = {}
        self.games_by_submission = {}
        self.debug = debug

    def add_new_game(self, new_game_id):
        self.games_by_id[new_game_id] = PicturePhoneGame(new_game_id, self, self.debug)

    def get_game_by_id(self, game_id):
        return self.games_by_id[game_id]

    def get_game_for_message(self, message):
        submission_id = self._get_message_id(message)
        return self.games_by_submission[submission_id]

    def put_game_for_message(self, message, game_to_put):
        submission_id = self._get_message_id(message)
        self.games_by_submission[submission_id] = game_to_put

    def _get_message_id(self, message):
        return message.message_id