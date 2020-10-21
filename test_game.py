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

    with pytest.raises(PicturePhoneGameError):
        game.start()


def test_player_cannot_join_game_twice():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game = game_with_players(players)

    with pytest.raises(PicturePhoneGameError):
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


def test_5():
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


### HELPERS ###

def game_with_players(players):
    game = PicturePhoneGame()

    for player in players:
        game.join_player(player)
    
    return game