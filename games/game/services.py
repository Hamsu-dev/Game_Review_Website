import datetime
from flask import session

from games.domainmodel.model import Game, Review, User
from games.adapters.repository import AbstractRepository

def get_game_data(repo: AbstractRepository, game_id):
    game = repo.get_game(game_id)
    # no, i refuse to do that weird game object to dict thing
    return game

def add_review(repo: AbstractRepository, game_id: int, rating: int, comment: str):
    user = repo.get_user(session['username'])
    game = repo.get_game(game_id)

    if check_if_reviewed(repo, game_id, user.username):
        raise ValueError

    rev = Review(user, game, rating, comment, datetime.date.today())
    user.add_review(rev)
    game.add_review(rev)
    repo.add_review(rev)


# Check if user has already reviewed this game
def check_if_reviewed(repo: AbstractRepository, game_id: int, username: str):
    user = repo.get_user(username)
    if user is None: return False

    for rev in user.reviews:
        if rev.game.game_id == game_id:
            return True

    return False
