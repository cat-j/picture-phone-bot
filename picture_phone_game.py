from bot_texts import BotTexts
from game_errors import *


class PicturePhoneGameResults:

    def __init__(self):
        self.contents = []

    def add_move(self, move):
        self.contents.append(move)


class PicturePhoneGameMove:

    def __init__(self, player_making_move, submission):
        self.player = player_making_move
        self.submission = submission

    def send_self(self, chat_id, context):
        raise NotImplementedError("Subclass responsibility")


class WritingMove(PicturePhoneGameMove):
    
    def send_self(self, chat_id, context):
        context.bot.send_message(chat_id=chat_id, text=self.submission)


class DrawingMove(PicturePhoneGameMove):
    
    def send_self(self, chat_id, context):
        context.bot.send_photo(chat_id=chat_id, photo=self.submission)


class PicturePhoneGameState:

    def __init__(self, debug=False):
        self.players = set()
        self.remaining_players = []
        self.started = False
        self.finished = False
        self.MIN_PLAYERS = 4
        self.debug = debug

    def join_player(self, joining_player):
        if not self._game_started():
            self._add_player(joining_player)
        else:
            raise PicturePhoneGameError("Cannot join game after it has started.")

    def start(self):
        if not self._game_started():
            if self._number_of_players() < self.MIN_PLAYERS:
                raise NotEnoughPlayersError(
                    "Cannot start game until at least {} players have joined.".format(self.MIN_PLAYERS)
                )
            self._set_remaining_players(self.players)
            self.started = True
            return True
        else:
            raise PicturePhoneGameError("Game already started.")

    def get_next_player(self):
        return self.remaining_players[0]

    def play_turn(self, player_making_move, submission):
        if self.finished:
            raise PicturePhoneGameError("Cannot play turn when game is already finished.")
        else:
            self.remaining_players = self.remaining_players[1:]
            if not self.remaining_players:
                self.finished = True

    ### PRIVATE ###

    def _game_started(self):
        return self.started

    def _set_remaining_players(self, players):
        self.remaining_players = list(players)
        return self.started

    def _add_player(self, joining_player):
        if not joining_player in self.players:
            self.players.add(joining_player)
        else:
            raise PlayerAlreadyJoinedError("Player {} is already in the game.".format(joining_player))

    def _number_of_players(self):
        return len(self.players)


class PicturePhoneGamePhase:

    def __init__(self, game):
        self.game = game
        self.game_state = self.game.game_state
        self.game_database = self.game.game_database

    def play_turn(self, message, context):
        if self.accepts_message(message):
            # User submission is valid! Store it and play turn.
            self.game_database.put_game_for_message(message, self.game)
            self.add_move(message)
            self.game_state.play_turn(
                player_making_move=message.from_user,
                submission=self.contents_for_phase(message)
            )
            context.bot.send_message(chat_id=message.chat.id, text=BotTexts.submission_received)
            self.game.advance_phase()
            try:
                self.send_message_to_next_player(message, context)
            except IndexError:
                context.bot.send_message(chat_id=self.game.group_id(), text="Game finished")
                self.game.send_results(context)
        else:
            context.bot.send_message(chat_id=message.chat.id, text=self.reply_to_invalid_message())

    def add_move(self, message):
        player_making_move = message.from_user.id
        move_class = self.move_class()
        move_to_add = move_class(player_making_move, self.contents_for_phase(message))
        self.game.add_move(move_to_add)

    def next_phase(self):
        raise NotImplementedError("Subclass responsiblity")

    def accepts_message(self, message):
        raise NotImplementedError("Subclass responsiblity")

    def contents_for_phase(self, message):
        raise NotImplementedError("Subclass responsiblity")

    def send_message_to_next_player(self, message, context):
        raise NotImplementedError("Subclass responsiblity")

    def reply_to_invalid_message(self):
        raise NotImplementedError("Subclass responsiblity")

    def move_class(self):
        raise NotImplementedError("Subclass responsiblity")


class WritingPhase(PicturePhoneGamePhase):

    def next_phase(self):
        return DrawingPhase(self.game)

    def accepts_message(self, message):
        return message.text

    def contents_for_phase(self, message):
        return message.text

    def send_message_to_next_player(self, message, context):
        self.game.send_text_to_next_player(message, context)

    def reply_to_invalid_message(self):
        return BotTexts.writing_phase_type_error

    def move_class(self):
        return WritingMove


class DrawingPhase(PicturePhoneGamePhase):

    def next_phase(self):
        return WritingPhase(self.game)

    def accepts_message(self, message):
        return message.photo

    def contents_for_phase(self, message):
        return message.photo[-1]

    def send_message_to_next_player(self, message, context):
        self.game.send_photo_to_next_player(message, context)

    def reply_to_invalid_message(self):
        return BotTexts.drawing_phase_type_error

    def move_class(self):
        return DrawingMove


class PicturePhoneGame:

    def __init__(self, game_id, game_database, debug):
        self.game_state = PicturePhoneGameState(debug=debug)
        self.game_database = game_database
        self.current_phase = self._initial_phase()
        self.results = PicturePhoneGameResults()
        self.game_id = game_id
        self.debug = debug

    def start(self, update, context):
        try:
            self.game_state.start()
            player_id = self.game_state.get_next_player()
            message = context.bot.send_message(chat_id=player_id, text=BotTexts.first_player)
            self.game_database.put_game_for_message(message, self)
        except NotEnoughPlayersError:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You must wait until {} players have joined!".format(self.min_players())
            )

    def join_user(self, joining_user_id, context):
        try:
            self.game_state.join_player(joining_user_id)
            self._debug("Player {} joined game {}".format(joining_user_id, self.game_id))
            context.bot.send_message(
                chat_id=joining_user_id,
                text="You've joined game {}.".format(self.game_id)
            )
        except PicturePhoneGameError:
            context.bot.send_message(chat_id=joining_user_id, text=BotTexts.already_joined)

    def play_turn(self, message, context):
        self._debug(message)
        try:
            self.current_phase.play_turn(message, context)
        except PicturePhoneGameError:
            context.bot.send_message(chat_id=message.chat.id, text="That game is already finished!")

    def min_players(self):
        return self.game_state.MIN_PLAYERS

    def advance_phase(self):
        self.current_phase = self.current_phase.next_phase()

    def add_move(self, move_to_add):
        self.results.add_move(move_to_add)

    def send_results(self, context):
        for result in self.results.contents:
            result.send_self(self.group_id(), context)

    def group_id(self):
        return self.game_id

    def _debug(self, message):
        if self.debug:
            print(message)

    def _initial_phase(self):
        return WritingPhase(self)


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