

# Test that the profile page redirects to the login page when not logged in
def test_profile_page_unloggedin(client):
    response = client.get('/profile')
    assert response.headers['Location'] == '/authentication/login'


# Test that the profile page works
def test_profile_page(client, auth):
    auth.login()

    # Test that the profile page loads
    response = client.get('/profile')
    assert response.status_code == 200
    assert b'Welcome ' + auth.username.encode('utf-8') + b'!' in response.data


# Test that a review on a game appears on the profile page
def test_profile_review(client, auth):
    auth.login()
    client.post('/game/457140', data={'comment': 'This game is great!', 'rating': 5})

    response = client.get('/profile')
    assert b'This game is great!' in response.data
