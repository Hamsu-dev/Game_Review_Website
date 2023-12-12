from werkzeug.security import generate_password_hash, check_password_hash

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User

class NameNotUniqueException(Exception):
    pass

class AuthenticationException(Exception):
    pass

class UnknownUserException(Exception):
    pass

def add_user(username: str, password: str, repo: AbstractRepository):
    if repo.get_user(username) is not None:
        raise NameNotUniqueException
    
    password_hash = generate_password_hash(password)
    user = User(username, password_hash)
    repo.add_user(user)

def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException
    return user

def authenticate_user(username: str, password: str, repo: AbstractRepository):
    user = get_user(username, repo)
    if user is None:
        raise UnknownUserException
    elif check_password_hash(user.password, password):
        return True
    raise AuthenticationException
