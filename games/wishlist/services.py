from math import ceil

import games.adapters.repository as repo
from games.domainmodel.model import Wishlist


GAMES_PER_PAGE = 15

def get_games_from_wishlist(wishlist, page):
    games = wishlist.list_of_games()
    games.sort(key=lambda x: x.title)
    max_page = ceil(len(games)/GAMES_PER_PAGE)
    games = games[(page-1)*GAMES_PER_PAGE:page*GAMES_PER_PAGE]
    return games, max_page
    