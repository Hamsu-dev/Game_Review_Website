from flask import session

import games.adapters.repository as repo

def get_short_wishlist():
    user = repo.repo_instance.get_user(session['username'])
    wishlist = user.wishlist
    games = wishlist.list_of_games()
    if len(games) > 3:
        return games[:3]
    else:
        return games

    
