import pytest

from games.domainmodel.model import *
from games.authentication import services as auth_services

# Certain aspects can't be automatically tested as csrf tokens are not sent for automated testing, however if we break authentication while working on other tings then it should be pretty obvious.

def test_add_user(repo):
    # Not technically a valid username/password combo, but this pair is in the database for easy testing.
    try:
        auth_services.add_user("test", "test", repo)
    except auth_services.NameNotUniqueException:
        assert True
    else:
        assert False
    
    # Invalid password shouldn't be added to the database.
    auth_services.add_user("testuser2", "test2", repo)
    assert repo.get_user("test2") is None

    # Invalid username/password is handled by the form, so we can't test it here.
    
    # Valid username/password should be added to the database.
    auth_services.add_user("testvaliduser", "Test123Password", repo)
    assert repo.get_user("testvaliduser") is not None

def test_get_user(repo):
    # Invalid username should raise an exception.
    try:
        auth_services.get_user("testuser", repo)
    except auth_services.UnknownUserException:
        assert True
    else:
        assert False
    
    # Adding a user to the database should allow us to get that user.
    auth_services.add_user("testuser", "Test123Password", repo)
    assert auth_services.get_user("testuser", repo) is not None

def test_authenticate_user(repo):
    # Invalid username should raise an exception.
    try:
        auth_services.authenticate_user("testuser", "Test123Password", repo)
    except auth_services.UnknownUserException:
        assert True
    else:
        assert False

    # Invalid password should raise an exception.
    u = ("testuser", "Test123Password")
    auth_services.add_user(u[0], u[1], repo)
    try:
        user = auth_services.authenticate_user(u[0], u[1]+"invalid", repo)
        assert user == None;
    except auth_services.AuthenticationException:
        assert True
    else:
        assert False
    
    # Valid username/password should return the user.
    assert auth_services.authenticate_user(u[0], u[1], repo)





