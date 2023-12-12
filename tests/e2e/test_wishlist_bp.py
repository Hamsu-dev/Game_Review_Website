import pytest

from flask import session

from games.domainmodel.model import *

def test_wishlist_page_unloggedin(client):
    response = client.get('/wishlist')
    assert response.headers['Location'] == '/authentication/login'

def test_adding_game_to_wishlist(repo, client, auth):
    auth.login()

    # Test wishlist starts empty
    response = client.get('/wishlist')
    assert b'Oxygen Not Included' not in response.data

    # Test adding game.
    client.post('/game/add_to_wishlist/457140')
    response = client.get('/wishlist')
    assert b'Oxygen Not Included' in response.data

    

def test_remove_from_wishlist_from_game_page(client, auth):
    auth.login()

    client.post('/game/add_to_wishlist/457140')

    # Test remove from wishlist
    client.post('/game/remove_from_wishlist/457140')
    response = client.get('/wishlist')
    assert b'Oxygen Not Included' not in response.data

def test_remove_from_wishlist_from_wishlist_page(client, auth):
    auth.login()

    client.post('/game/add_to_wishlist/457140')

    # Test remove from wishlist
    client.post('/wishlist/remove/457140')
    response = client.get('/wishlist')
    assert b'Oxygen Not Included' not in response.data