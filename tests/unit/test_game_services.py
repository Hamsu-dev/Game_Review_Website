import pytest

from games.game import services as game_services


def test_game_service_getting_invalid_game_data(repo):
    # Games with these IDs do not exist, so the service should return None.
    game_data = game_services.get_game_data(repo, 1)
    assert game_data is None

    game_data = game_services.get_game_data(repo, -1)
    assert game_data is None


def test_game_service_getting_vaild_game_data(repo):
    # These games exist, and the games service should be able to get their data.
    game_data = game_services.get_game_data(repo, 457140)
    assert game_data.title == "Oxygen Not Included"
    assert game_data.developer == "Klei Entertainment"

    game_data = game_services.get_game_data(repo, 40800)
    assert game_data.title == "Super Meat Boy"
    assert game_data.developer == "Team Meat"


# def test_game_service_adding_review(repo):
#     # Test that a review can be added to a game.
#     game_services.add_review(repo, 457140, 5, "This game is great!")
#     game_data = game_services.get_game_data(repo, 457140)
#     assert len(game_data.reviews) == 1
#     assert game_data.reviews[0].comment == "This game is great!"

#     game_services.add_review(repo, 457140, 1, "This game is terrible!")
#     game_data = game_services.get_game_data(repo, 457140)
#     assert len(game_data.reviews) == 2
#     assert game_data.reviews[1].comment == "This game is terrible!"


# def test_game_service_check_if_reviewed(repo):
#     # Test that the service can check if a user has already reviewed a game.
#     game_services.add_review(repo, 457140, 5, "This game is great!")
#     assert game_services.check_if_reviewed(repo, 457140, "thorke") is True
#     assert game_services.check_if_reviewed(repo, 457140, "fmercury") is False
#     assert game_services.check_if_reviewed(repo, 457140, "pmccartney") is False

#     game_services.add_review(repo, 457140, 1, "This game is terrible!")
#     assert game_services.check_if_reviewed(repo, 457140, "thorke") is True
#     assert game_services.check_if_reviewed(repo, 457140, "fmercury") is False
#     assert game_services.check_if_reviewed(repo, 457140, "pmccartney") is False
