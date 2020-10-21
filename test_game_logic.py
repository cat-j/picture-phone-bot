import pytest

from picture_phone_game import (
    PicturePhoneGameLogic,
    PicturePhoneGameError
)


def test_game_can_start_with_at_least_four_players():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game_logic = PicturePhoneGameLogic(players)

    assert game_logic.next_player() in players
    assert not game_logic.finished


def test_game_starts_with_writing_phase():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game_logic = PicturePhoneGameLogic(players)

    assert game_logic.current_phase == "WRITING"


def test_after_writing_comes_drawing():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game_logic = PicturePhoneGameLogic(players)
    
    play_turn_and_get_next_player(game_logic, "A cocobolo desk")

    assert game_logic.current_phase == "DRAWING"


def test_game_finishes_in_correct_number_of_turns():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game_logic = PicturePhoneGameLogic(players)

    for i in range(0, len(players)):
        assert not game_logic.finished
        game_logic.play_turn(game_logic.next_player(), "A cocobolo desk")

    assert game_logic.finished


def test_cannot_play_finished_game():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game_logic = PicturePhoneGameLogic(players)

    while not game_logic.finished:
        game_logic.play_turn(game_logic.next_player(), "A cocobolo desk")

    with pytest.raises(PicturePhoneGameError):
        game_logic.play_turn("Jimmy McGill", "A cocobolo desk")


def test_everyone_gets_to_play():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    already_played = []
    game_logic = PicturePhoneGameLogic(players)

    while not game_logic.finished:
        next_player = play_turn_and_get_next_player(game_logic, "A cocobolo desk")
        already_played.append(next_player)

    for player in already_played:
        assert player in players

    for player in players:
        assert player in already_played


def test_game_results_are_stored_in_order():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    submissions = [
        "A cocobolo desk",
        "Two cocobolo desks",
        "Three cocobolo desks",
        "Four cocobolo desks"
    ]
    already_played = []
    game_logic = PicturePhoneGameLogic(players)

    for submission in submissions:
        next_player = play_turn_and_get_next_player(game_logic, submission)
        already_played.append(next_player)

    game_results = game_logic.results()

    assert game_results.players_in_order() == already_played
    assert game_results.submissions_in_order() == submissions


def test_0():
    game_logic = PicturePhoneGameLogic()
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]

    with pytest.raises(PicturePhoneGameError):
        game_logic.next_player()
    
    game_logic.set_players(players)

    assert game_logic.next_player() in players


### HELPERS ###

def play_turn_and_get_next_player(game_to_play, submission_for_turn):
    next_player = game_to_play.next_player()
    game_to_play.play_turn(next_player, submission_for_turn)
    return next_player