import pytest

from picture_phone_game import (
    PicturePhoneGame,
    PicturePhoneGameError
)


def test_0():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game = PicturePhoneGame()

    for player in players:
        game.join_player(player)

    start = game.start()

    assert start


def test_1():
    players = [
        "Mike Ehrmantraut",
        "Stacey Ehrmantraut",
        "Kaylee Ehrmantraut"
    ]
    game = PicturePhoneGame()

    for player in players:
        game.join_player(player)

    with pytest.raises(PicturePhoneGameError):
        game.start()


def test_2():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game = PicturePhoneGame()

    for player in players:
        game.join_player(player)

    with pytest.raises(PicturePhoneGameError):
        game.join_player(players[0])


def test_3():
    players = [
        "Jimmy McGill",
        "Kim Wexler",
        "Howard Hamlin",
        "Chuck McGill"
    ]
    game = PicturePhoneGame()

    for player in players:
        game.join_player(player)

    game.start()

    with pytest.raises(PicturePhoneGameError):
        game.join_player("Rick Schweikart")