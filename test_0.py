import pytest

from picture_phone_game import (
    PicturePhoneGame,
    PicturePhoneGameError
)


def test_game_can_start_with_at_least_four_players():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game_with_four_players = PicturePhoneGame(players)

    assert game_with_four_players.next_player() in players
    assert not game_with_four_players.finished


def test_game_cannot_start_with_less_than_four_players():
    players = [
        "Mike Ehrmantraut",
        "Stacey Ehrmantraut",
        "Kaylee Ehrmantraut"
    ]

    with pytest.raises(ValueError):
        PicturePhoneGame(players)


def test_game_starts_with_writing_phase():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game_with_four_players = PicturePhoneGame(players)

    assert game_with_four_players.current_phase == "WRITING"


def test_after_writing_comes_drawing():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game_with_four_players = PicturePhoneGame(players)
    next_player = game_with_four_players.next_player()
    game_with_four_players.play_turn(next_player, "A cocobolo desk")

    assert game_with_four_players.current_phase == "DRAWING"


def test_game_finishes_in_correct_number_of_turns():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game_with_four_players = PicturePhoneGame(players)

    for i in range(0, len(players)):
        assert not game_with_four_players.finished
        game_with_four_players.play_turn(game_with_four_players.next_player(), "A cocobolo desk")

    assert game_with_four_players.finished


def test_cannot_play_finished_game():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game_with_four_players = PicturePhoneGame(players)

    for i in range(0, len(players)):
        game_with_four_players.play_turn(game_with_four_players.next_player(), "A cocobolo desk")

    with pytest.raises(PicturePhoneGameError):
        game_with_four_players.play_turn("Jimmy McGill", "A cocobolo desk")


def test_everyone_gets_to_play():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    already_played = []
    game_with_four_players = PicturePhoneGame(players)

    while not game_with_four_players.finished:
        next_player = game_with_four_players.next_player()
        game_with_four_players.play_turn(next_player, "A cocobolo desk")
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
    game_with_four_players = PicturePhoneGame(players)

    for submission in submissions:
        next_player = game_with_four_players.next_player()
        game_with_four_players.play_turn(next_player, submission)
        already_played.append(next_player)

    game_results = game_with_four_players.results()

    assert game_results.players_in_order() == already_played
    assert game_results.submissions_in_order() == submissions