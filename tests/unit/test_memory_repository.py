import pytest

from games.adapters.memory_repository import MemoryRepository, populate
from games.domainmodel.model import Game, Genre, Publisher, Tag

def test_adding_games():
    repo = MemoryRepository()
    assert repo.get_number_of_games() == 0
    game1 = Game(1, 'a')
    game2 = Game(2, 'b')
    game3 = Game(3, 'c')
    repo.add_game(game1)
    assert repo.get_number_of_games() == 1
    repo.add_game(game2)
    assert repo.get_number_of_games() == 2
    repo.add_game(game3)
    assert repo.get_number_of_games() == 3
    assert repo.get_game(1) == game1
    assert repo.get_game(2) == game2
    assert repo.get_game(3) == game3
    assert repo.get_game(4) == None
    assert repo.get_games() == [game1, game2, game3]

def test_adding_genres():
    repo = MemoryRepository()
    assert repo.get_genres() == []
    genre1 = Genre('genre a')
    genre2 = Genre('genre b')
    genre3 = Genre('genre c')
    repo.add_genre(genre1)
    assert repo.get_genres() == [genre1]
    repo.add_genre(genre2)
    assert repo.get_genres() == [genre1, genre2]

def test_adding_tags():
    repo = MemoryRepository()
    assert repo.get_tags() == []
    tag_a, tag_b, tag_c = Tag('tag a'), Tag('tag b'), Tag('tag c')
    repo.add_tag(tag_a)
    assert repo.get_tags() == [tag_a]
    repo.add_tag(tag_b)
    assert repo.get_tags() == [tag_a, tag_b]
    repo.add_tag(tag_a)
    assert repo.get_tags() == [tag_a, tag_b]
    assert repo.get_tags() != [tag_b, tag_a]
    assert tag_c not in repo.get_tags()

def test_populate():
    # Check that the repo is empty before populating
    repo = MemoryRepository()
    assert repo.get_number_of_games() == 0
    assert repo.get_genres() == []
    assert repo.get_tags() == []
    
    # Populate the repo
    populate("tests/data/", repo) # Need to check how I'm supposed to access config.TEST_DATA_PATH

    # Check that the repo has games in it.
    assert repo.get_number_of_games() == 20
    assert repo.get_game(7940) == Game(7940, "Call of Duty® 4: Modern Warfare®")

    # Check that the repo has genres in it.
    assert Genre('Action') in repo.get_genres()
    assert Genre('Adventure') in repo.get_genres()
    assert Genre('Casual') in repo.get_genres()
    assert Genre('not a real genre') not in repo.get_genres()

    # Check that the repo has tags in it.
    assert Tag('2d') in repo.get_tags()
    assert Tag('3d') in repo.get_tags()
    assert Tag('not a real tag') not in repo.get_tags()

def test_search_games():
    repo = MemoryRepository()
    populate("tests/data/", repo)

    # Checking searching by title
    a_games = repo.search_games(title='a')
    for game in a_games:
        assert 'a' in game.title.lower()
    b_games = repo.search_games(title='b')
    for game in b_games:
        assert 'b' in game.title.lower()

    # Checking searching by price
    free_games = repo.search_games(price=0)
    for game in free_games:
        assert game.price == 0
    cheap_games = repo.search_games(price=1)
    for game in cheap_games:
        assert game.price <= 1
    
    # Checking searching by genre
    action_games = repo.search_games(genre='Action')
    for game in action_games:
        assert Genre('Action') in game.genres
    adventure_games = repo.search_games(genre='Adventure')
    for game in adventure_games:
        assert Genre('Adventure') in game.genres
