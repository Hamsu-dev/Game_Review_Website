from datetime import date, datetime

from werkzeug.security import generate_password_hash

import pytest

import games.adapters.repository as repo
from games.adapters.database_repository import DatabaseRepository
from games.domainmodel.model import User, Game, Publisher, Genre, Tag, Review
from games.adapters.repository import RepositoryException

def test_repository_can_add_a_user(session_factory):
    repo = DatabaseRepository(session_factory)

    user = User("Alex", generate_password_hash("MyReallySecurePassword123"))
    repo.add_user(user)
    
    assert repo.get_user("Alex") == user

def test_repository_can_retrieve_a_user(session_factory):
    repo = DatabaseRepository(session_factory)

    user = repo.get_user("test")
    assert user == User("test", generate_password_hash("test"))

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = DatabaseRepository(session_factory)

    user = repo.get_user("test2")
    assert user is None

def test_repository_can_retrieve_game_count(session_factory):
    repo = DatabaseRepository(session_factory)

    assert repo.get_number_of_games() == 20

def test_repository_can_add_a_game(session_factory):
    repo = DatabaseRepository(session_factory)

    game = Game(1, "Super Cool Game!")
    game.price = 42
    game.release_date = "Oct 31, 1701"
    game.description = "This game is super cool!"
    game.image_url = "https://via.placeholder.com/1024x512"
    game.add_genre(Genre("Action"))
    game.add_genre(Genre("Adventure"))
    game.publisher = Publisher("Alex")
    game.add_tag(Tag("2d"))
    game.add_tag(Tag("newtag"))
    game.recommendations = 3
    game.windows = True
    game.achievements = 100
    game.developer = "Alex the dev"

    repo.add_game(game)

    assert repo.get_game(1) == game
    assert repo.get_number_of_games() == 21
    assert repo.get_game(1).description == "This game is super cool!"
    assert repo.get_game(1).image_url == "https://via.placeholder.com/1024x512"
    assert Genre("Action") in repo.get_game(1).genres
    assert Genre("Adventure") in repo.get_game(1).genres
    assert repo.get_game(1).publisher == Publisher("Alex")
    assert Tag("2d") in repo.get_game(1).tags
    assert Tag("newtag") in repo.get_game(1).tags
    assert Tag("newtag") in repo.get_tags()
    assert repo.get_game(1).recommendations == 3
    assert repo.get_game(1).windows == True
    assert repo.get_game(1).achievements == 100
    assert repo.get_game(1).developer == "Alex the dev"

def test_repository_can_retrieve_a_game(session_factory):
    repo = DatabaseRepository(session_factory)

    game = repo.get_game(457140)
    assert game.title == "Oxygen Not Included"
    assert game.price == 124.99
    assert game.publisher == Publisher("Klei Entertainment")

def test_repository_does_not_retrieve_a_non_existent_game(session_factory):
    repo = DatabaseRepository(session_factory)

    game = repo.get_game(0)
    assert game is None

def test_repository_can_retrieve_genres(session_factory):
    repo = DatabaseRepository(session_factory)

    genres = repo.get_genres()
    assert len(genres) == 7

def test_repository_can_add_reviews(session_factory):
    repo = DatabaseRepository(session_factory)
    
    game = repo.get_game(457140)
    user = repo.get_user("test")
    review = Review(user, game, 5, "wow, I love this game!", datetime.now())
    game.add_review(review)
    user.add_review(review)
    repo.add_review(review)

    assert repo.get_game(457140).reviews[0] == review
    assert repo.get_game(457140).reviews[0].user == user
    assert repo.get_user("test").reviews[0] == review
