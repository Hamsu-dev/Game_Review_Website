import pytest


def test_game_page(client):
    # Test that the game page returns the correct games
    response = client.get('/game/457140')
    assert response.status_code == 200
    assert b'Oxygen Not Included' in response.data
    assert b'124.99' in response.data

    response = client.get('/game/40800')
    assert response.status_code == 200
    assert b'Super Meat Boy' in response.data
    assert b'114.99' in response.data


def test_invaild_game_page(client):
    # The web app should show a 404 page when the game doesn't exist/isn't found
    response = client.get('/game/1')
    assert response.status_code == 404

    response = client.get('/game/-1')
    assert response.status_code == 404


###############
# REVIEW TESTS
###############

# The web app should redirect to the login page when trying to review a game while not logged in
def test_unloggedin_review(client):
    response = client.post('/game/457140', data={'comment': 'This game is great!', 'rating': 5})
    assert response.headers['Location'] == '/authentication/login'


# Tests normal review
def test_review(client, auth):
    auth.login()
    response = client.post('/game/457140', data={'comment': 'I really love playing this game!', 'rating': 5})

    # The review should be on the game's page now
    assert b'I really love playing this game!' in response.data


# Tests reviews with abnormal inputs
@pytest.mark.parametrize(('comment', 'rating', 'message'), (
    ('a', 5, b'The review is too short! Please try to be more descriptive'),
    ('This is my rating', 10, b'Rating must be between 1 and 5'),
))
def test_review_abnormal_inputs(client, auth, comment, rating, message):
    auth.login()

    response = client.post('/game/457140', data={'comment': comment, 'rating': rating})
    assert message in response.data


def test_multiple_reviews(client, auth):
    auth.login()

    response = client.post('/game/457140', data={'comment': 'My first review', 'rating': 5})
    assert b'My first review' in response.data
    assert b'You have already reviewed this game' in response.data

    response = client.post('/game/457140', data={'comment': 'My second review', 'rating': 5})
    assert b'My first review' in response.data

    response = client.get('/game/457140')
    assert not (b'My second review' in response.data)
