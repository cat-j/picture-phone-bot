WRITING = "WRITING"
DRAWING = "DRAWING"


class PicturePhoneGame:

    def __init__(self, players):
        if len(players) < 4:
            raise ValueError("Must have at least 4 players.")

        self.players = players
        self.finished = False
        self.current_phase = self._starting_phase()
        self.moves = PicturePhoneGameResults()

    def next_player(self):
        return self.players[0]

    def play_turn(self, player_making_move, submission):
        if self.finished:
            raise PicturePhoneGameError("Cannot play turn when game is already finished.")
        else:
            self._advance_phase()
            self.moves.add_move(player_making_move, submission)
            self.players = self.players[1:]
            if not self.players:
                self.finished = True

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


class PicturePhoneGameResults:

    def __init__(self):
        self.contents = []

    def add_move(self, player_making_move, submission):
        self.contents.append((player_making_move, submission))

    def players_in_order(self):
        return [move[0] for move in self.contents]

    def submissions_in_order(self):
        return [move[1] for move in self.contents]