import pytest

from game_errors import *
from picture_phone_game import (
    PicturePhoneGameState,
    PicturePhoneGameError,
    PlayerAlreadyJoinedError,
    NotEnoughPlayersError
)


def test_game_can_start_with_at_least_four_players():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game = game_with_players(players)

    start = game.start()

    assert start


def test_game_cannot_start_with_less_than_four_players():
    players = [
        "Mike Ehrmantraut",
        "Stacey Ehrmantraut",
        "Kaylee Ehrmantraut"
    ]
    game = game_with_players(players)

    with pytest.raises(NotEnoughPlayersError):
        game.start()


def test_player_cannot_join_game_twice():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game = game_with_players(players)

    with pytest.raises(PlayerAlreadyJoinedError):
        game.join_player(players[0])


def test_player_cannot_join_game_already_in_course():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game = game_with_players(players)

    game.start()

    with pytest.raises(PicturePhoneGameError):
        game.join_player("Rick Schweikart")


def test_cannot_start_already_started_game():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game = game_with_players(players)

    game.start()

    with pytest.raises(PicturePhoneGameError):
        game.start()


def test_next_player_is_valid():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game = game_with_players(players)

    game.start()

    assert game.get_next_player() in players

### HELPERS ###

def game_with_players(players):
    game = PicturePhoneGameState()

    for player in players:
        game.join_player(player)
    
    return game