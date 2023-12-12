import pytest

from games.domainmodel.model import *
from games.browse import services as browse_services


@pytest.fixture
def list_of_games():
    game1 = Game(1, 'a')
    game1.price = 1.0
    game1.release_date = 'Nov 12, 2007'
    game1.publisher = Publisher("publisher a")
    game1.add_genre(Genre('genre a'))
    game1.recommendations = 10

    game2 = Game(2, 'b')
    game2.price = 1.2
    game2.release_date = 'Nov 13, 2007'
    game2.publisher = Publisher("publisher b")
    game2.add_genre(Genre('genre a'))
    game2.add_genre(Genre('genre b'))
    game2.recommendations = 5

    game3 = Game(3, 'c')
    game3.price = 0.9
    game3.release_date = 'Nov 14, 2007'
    game3.publisher = Publisher("publisher c")
    game3.add_genre(Genre('genre b'))
    game3.recommendations = 15

    return [game1, game2, game3]


def test_sort_games(list_of_games):
    # Checking that games are in correct order after sorting.
    browse_services.sort_games(list_of_games, 'price')
    assert list_of_games[0] == Game(3, 'c')
    assert list_of_games[1] == Game(1, 'a')
    assert list_of_games[2] == Game(2, 'b')

    browse_services.sort_games(list_of_games, 'title')
    assert list_of_games[0] == Game(1, 'a')
    assert list_of_games[1] == Game(2, 'b')
    assert list_of_games[2] == Game(3, 'c')

    browse_services.sort_games(list_of_games, 'popular')
    assert list_of_games[0] == Game(3, 'c')
    assert list_of_games[1] == Game(1, 'a')
    assert list_of_games[2] == Game(2, 'b')

def test_search_games(repo):
    # Note that search_games also handles pagination, so the returned list will always have 15 games (or less if we're on the final page). This is also why we need to return num_games alongside the list of games.
    # Checking searching by title
    a_games, num_games = browse_services.search_games(repo, title='a')
    for game in a_games:
        assert 'a' in game.title.lower()
    b_games, num_games = browse_services.search_games(repo, title='b')
    for game in b_games:
        assert 'b' in game.title.lower()

    # Checking searching by price
    free_games, num_games = browse_services.search_games(repo, price=0)
    for game in free_games:
        assert game.price == 0
    cheap_games, num_games = browse_services.search_games(repo, price=1)
    for game in cheap_games:
        assert game.price <= 1
    
    # Checking searching by genre
    action_games, num_games = browse_services.search_games(repo, genre='Action')
    for game in action_games:
        assert Genre('Action') in game.genres
    adventure_games, num_games = browse_services.search_games(repo, genre='Adventure')
    for game in adventure_games:
        assert Genre('Adventure') in game.genres
    
    # Checking pages
    all_games_page_1, num_games = browse_services.search_games(repo, page=1)
    assert len(all_games_page_1) == 15
    all_games_page_2, num_games = browse_services.search_games(repo, page=2)
    assert len(all_games_page_2) == 5
    # 20 games in total, 15 on page 1, 5 on page 2
    for game in all_games_page_1:
        assert game not in all_games_page_2
    for game in all_games_page_2:
        assert game not in all_games_page_1


    
