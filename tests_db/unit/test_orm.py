import datetime
import pickle
import pytest
from sqlalchemy.exc import IntegrityError

from games.domainmodel.model import User, Game, Tag, Review, Genre, Publisher


def add_user(sess, account=None):
    new_name = "Bob"
    new_password = "avodaco"
    if account is not None:
        new_name = account[0]
        new_password = account[1]

    sess.execute(
        'INSERT INTO users (username, password) VALUES (:username, :password)',
        {'username': new_name, 'password': new_password}
    )
    return sess.execute(
        'SELECT id from users where username = :username',
        {'username': new_name}
    ).fetchone()[0]


def add_users(sess, accounts):
    for value in accounts:
        sess.execute(
            'INSERT INTO users (username, password) VALUES (:username, :password)',
            {'username': value[0], 'password': value[1]}
        )
    return tuple(row[0] for row in list(sess.execute('SELECT id from users')))


def add_game(sess, publisher_name=None):
    sess.execute(
        'INSERT INTO games (game_id, game_title, price, release_date, description, image_url, website_url, recommendations, windows, mac, linux, categories, achievements, developer, screenshots, movies) VALUES (:game_id, :game_title, :price, :release_date, :description, :image_url, :website_url, :recommendations, :windows, :mac, :linux, :categories, :achievements, :developer, :screenshots, :movies)',
        {
            'game_id': 1,
            'game_title': "Test Game",
            'price': 9.99,
            'release_date': "Jun 1, 2010",
            'description': "This is a test game",
            'image_url': "https://example.com",
            'website_url': "https://example.com",
            'recommendations': 100,
            'windows': True,
            'mac': True,
            'linux': False,
            'categories': pickle.dumps(['Action']),
            'achievements': 10,
            'developer': "Test Developer",
            'screenshots': pickle.dumps(['https://example.com']),
            'movies': pickle.dumps(['https://example.com'])
        }
    )
    
    if publisher_name is not None:
        sess.execute(
            'UPDATE games SET publisher_name = :publisher WHERE game_id = :game_id',
            {
                'publisher': publisher_name,
                'game_id': 1
            }
        )

    return sess.execute(
        'SELECT game_id from games where game_title = :game_title',
        {'game_title': "Test Game"}
    ).fetchone()[0]


def add_publisher(sess):
    sess.execute(
        'INSERT INTO publishers (name) VALUES ("Test Publisher")'
    )
    return sess.execute(
        'SELECT name from publishers'
    ).fetchone()[0]


def add_tags(sess):
    sess.execute(
        'INSERT INTO tags (tag_name) VALUES ("Action"), ("Adventure")'
    )
    return tuple(row[0] for row in list(sess.execute('SELECT tag_name from tags')))


def add_game_tag_associations(sess, game_id, tag_names):
    for tag_name in tag_names:
        sess.execute(
            'INSERT INTO game_tags (game_id, tag_name) VALUES (:game_id, :tag_name)',
            {
                'game_id': game_id,
                'tag_name': tag_name
            }
        )


def add_genres(sess):
    sess.execute(
        'INSERT INTO genres (genre_name) VALUES ("Action"), ("Adventure")'
    )
    return tuple(row[0] for row in list(sess.execute('SELECT genre_name from genres')))


def add_game_genre_associations(sess, game_id, genre_names):
    for genre_name in genre_names:
        sess.execute(
            'INSERT INTO game_genres (game_id, genre_name) VALUES (:game_id, :genre_name)',
            {
                'game_id': game_id,
                'genre_name': genre_name
            }
        )


def add_reviewed_game(sess):
    sess.execute(
        'INSERT INTO reviews (user_id, game_id, rating, comment, date) VALUES (:user_id, :game_id, :rating, :comment, :date)',
        {
            'user_id': add_game(sess),
            'game_id': add_user(sess),
            'rating': 5,
            'comment': "This is a test review",
            'date': datetime.date(2020, 10, 10)
        }
    )

    return sess.execute('SELECT game_id from games').fetchone()[0]


def add_wishlist(sess, user_id, game_id):
    sess.execute(
        'INSERT INTO wishlists (user_id) VALUES (:user_id)',
        {'user_id': user_id}
    )
    wishlist_id = sess.execute('SELECT id from wishlists').fetchone()[0]

    sess.execute(
        'INSERT INTO wishlist_games (wishlist_id, game_id) VALUES (:wishlist_id, :game_id)',
        {
            'wishlist_id': wishlist_id,
            'game_id': game_id
        }
    )

    return wishlist_id


def test_loading_of_users(empty_session):
    add_users(empty_session, [
        ("Andrew", "Avocado101"),
        ("Cindy", "Cinderella99")
    ])

    assert empty_session.query(User).all() == [
        User("Andrew", "Avocado101"),
        User("Cindy", "Cinderella99")
    ]


def test_saving_of_users(empty_session):
    user = User("Andrew", "Avocado101")
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("Andrew", "Avocado101")]


def test_loading_of_game(empty_session):
    add_game(empty_session)

    rows = empty_session.query(Game).all()
    game = rows[0]
    
    expected_game = Game(1, "Test Game")
    assert game == expected_game

    assert game.game_id == 1
    assert game.title == "Test Game"
    assert game.price == 9.99
    assert game.release_date == "Jun 1, 2010"
    assert game.description == "This is a test game"
    assert game.image_url == "https://example.com"
    assert game.website_url == "https://example.com"
    assert game.recommendations == 100
    assert game.windows == 1
    assert game.mac == 1
    assert game.linux == 0
    assert game.categories == ['Action']
    assert game.achievements == 10
    assert game.developer == "Test Developer"
    assert game.screenshots == ["https://example.com"]
    assert game.movies == ["https://example.com"]


def test_loading_of_publisher(empty_session):
    add_publisher(empty_session)

    rows = empty_session.query(Publisher).all()
    publisher = rows[0]

    assert publisher.publisher_name == "Test Publisher"


def test_loading_of_game_with_publisher(empty_session):
    publisher_name = add_publisher(empty_session)
    game_id = add_game(empty_session, publisher_name)

    game = empty_session.query(Game).get(game_id)
    publisher = empty_session.query(Publisher).get(publisher_name)

    assert game.publisher == publisher


def test_loading_of_tagged_game(empty_session):
    game_id = add_game(empty_session)
    tag_names = add_tags(empty_session)
    add_game_tag_associations(empty_session, game_id, tag_names)

    game = empty_session.query(Game).get(game_id)
    tags = [empty_session.query(Tag).get(key) for key in tag_names]

    for tag in tags:
        assert tag in game.tags


def test_loading_of_game_with_genre(empty_session):
    game_id = add_game(empty_session)
    genre_names = add_genres(empty_session)
    add_game_genre_associations(empty_session, game_id, genre_names)

    game = empty_session.query(Game).get(game_id)
    genres = [empty_session.query(Genre).get(key) for key in genre_names]

    for genre in genres:
        assert genre in game.genres


def test_loading_of_reviewed_game(empty_session):
    add_reviewed_game(empty_session)
    
    game = empty_session.query(Game).all()[0]
    
    for review in game.reviews:
        assert review.game is game


def test_loading_of_wishlist(empty_session):
    user_id = add_user(empty_session)
    game_id = add_game(empty_session)
    wishlist_id = add_wishlist(empty_session, user_id, game_id)
    
    user = empty_session.query(User).all()[0]
    game = empty_session.query(Game).all()[0]
    
    user.wishlist.add_game(game)
    
    empty_session.add(user)
    empty_session.commit()
    
    rows = list(empty_session.execute('SELECT user_id FROM wishlists'))
    assert rows == [
        (user_id,)
    ]
    
    rows = list(empty_session.execute('SELECT wishlist_id, game_id FROM wishlist_games'))
    assert rows == [
        (wishlist_id, game_id)
    ]


def test_saving_of_review(empty_session):
    game_id = add_game(empty_session)
    user_id = add_user(empty_session)
    
    game = empty_session.query(Game).all()[0]
    user = empty_session.query(User).all()[0]
    
    review = Review(user, game, 5, "This is a test review", datetime.date(2020, 10, 10))
    user.add_review(review)
    game.add_review(review)

    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, game_id, rating, comment, date FROM reviews'))
    assert rows == [
        (user_id, game_id, 5, "This is a test review", datetime.date(2020, 10, 10).isoformat())
    ]


def test_saving_of_game(empty_session):
    game = Game(1, "Test Game")
    game.price = 2.99
    game.release_date = "Oct 21, 2008"
    game.description = "This is a description"
    game.image_url = "https://example.com"
    game.website_url = "https://example.com"
    game.recommendations = 100
    game.windows = True
    game.mac = True
    game.linux = False
    game.categories = ['Action']
    game.achievements = 10
    game.developer = "Test Developer"
    game.screenshots = ["https://example.com"]
    game.movies = ["https://example.com"]
    empty_session.add(game)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT game_id, game_title, price FROM games'))
    assert rows == [
        (1, "Test Game", 2.99)
    ]
    

def test_saving_of_publisher(empty_session):
    publisher = Publisher("Test Publisher")
    empty_session.add(publisher)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT name FROM publishers'))
    assert rows == [
        ("Test Publisher",)
    ]
    

def test_saving_of_game_with_publisher(empty_session):
    game = Game(1, "Test Game")
    game.price = 2.99
    game.release_date = "Oct 21, 2008"
    game.description = "This is a description"
    game.image_url = "https://example.com"
    game.website_url = "https://example.com"
    game.recommendations = 100
    game.windows = True
    game.mac = True
    game.linux = False
    game.categories = ['Action']
    game.achievements = 10
    game.developer = "Test Developer"
    game.screenshots = ["https://example.com"]
    game.movies = ["https://example.com"]
    publisher = Publisher("Test Publisher")
    game.publisher = publisher

    empty_session.add(game)
    empty_session.commit()

    # Test already exists for this
    game_id = list(empty_session.execute('SELECT game_id FROM games'))[0][0]
    publisher_name = list(empty_session.execute('SELECT name FROM publishers'))[0][0]

    # Check that the game has publisher in games table
    rows = list(empty_session.execute('SELECT game_id, game_title, publisher_name FROM games'))
    assert rows == [
        (game_id, "Test Game", publisher_name)
    ]

    # Check that the publishers table has a new record
    rows = list(empty_session.execute('SELECT name FROM publishers'))
    assert rows == [
        (publisher_name,)
    ]


def test_saving_tagged_game(empty_session):
    game = Game(1, "Test Game")
    game.price = 2.99
    game.release_date = "Oct 21, 2008"
    game.description = "This is a description"
    game.image_url = "https://example.com"
    game.website_url = "https://example.com"
    game.recommendations = 100
    game.windows = True
    game.mac = True
    game.linux = False
    game.categories = ['Action']
    game.achievements = 10
    game.developer = "Test Developer"
    game.screenshots = ["https://example.com"]
    game.movies = ["https://example.com"]
    tag = Tag("Action")
    game.add_tag(tag)

    empty_session.add(game)
    empty_session.commit()

    # Test already exists for this
    game_id = list(empty_session.execute('SELECT game_id FROM games'))[0][0]

    # Check that the tags table has a new record
    tag_name = list(empty_session.execute('SELECT tag_name FROM game_tags'))[0][0]
    assert tag_name == "Action"

    # Check that the game_tags table has a new record
    rows = list(empty_session.execute('SELECT game_id, tag_name FROM game_tags'))
    game_foreign_key = rows[0][0]
    tag_foreign_key = rows[0][1]

    assert game_id == game_foreign_key
    assert tag_name == tag_foreign_key
    

def test_saving_game_with_genre(empty_session):
    game = Game(1, "Test Game")
    game.price = 2.99
    game.release_date = "Oct 21, 2008"
    game.description = "This is a description"
    game.image_url = "https://example.com"
    game.website_url = "https://example.com"
    game.recommendations = 100
    game.windows = True
    game.mac = True
    game.linux = False
    game.categories = ['Action']
    game.achievements = 10
    game.developer = "Test Developer"
    game.screenshots = ["https://example.com"]
    game.movies = ["https://example.com"]
    genre = Genre("Action")
    game.add_genre(genre)

    empty_session.add(game)
    empty_session.commit()

    # Test already exists for this
    game_id = list(empty_session.execute('SELECT game_id FROM games'))[0][0]

    # Check that the genres table has a new record
    genre_name = list(empty_session.execute('SELECT genre_name FROM game_genres'))[0][0]
    assert genre_name == "Action"

    # Check that the game_genres table has a new record
    rows = list(empty_session.execute('SELECT game_id, genre_name FROM game_genres'))
    game_foreign_key = rows[0][0]
    genre_foreign_key = rows[0][1]

    assert game_id == game_foreign_key
    assert genre_name == genre_foreign_key


def test_saving_reviewed_game(empty_session):
    game = Game(1, "Test Game")
    game.price = 2.99
    game.release_date = "Oct 21, 2008"
    game.description = "This is a description"
    game.image_url = "https://example.com"
    game.website_url = "https://example.com"
    game.recommendations = 100
    game.windows = True
    game.mac = True
    game.linux = False
    game.categories = ['Action']
    game.achievements = 10
    game.developer = "Test Developer"
    game.screenshots = ["https://example.com"]
    game.movies = ["https://example.com"]

    user = User("Andrew", "Avocado101")

    review = Review(user, game, 5, "This is a test review", datetime.date(2020, 10, 10))
    user.add_review(review)
    game.add_review(review)
    
    empty_session.add(game)
    empty_session.commit()
    
    # Test already exists for this
    game_id = list(empty_session.execute('SELECT game_id FROM games'))[0][0]
    
    # Test already exists for this
    user_id = list(empty_session.execute('SELECT id FROM users'))[0][0]
    
    # Check that the reviews table has a new record
    rows = list(empty_session.execute('SELECT user_id, game_id, rating, comment, date FROM reviews'))
    assert rows == [
        (user_id, game_id, 5, "This is a test review", datetime.date(2020, 10, 10).isoformat())
    ]

def test_saving_wishlisted_game(empty_session):
    game = Game(1, "Test Game")
    game.price = 2.99
    game.release_date = "Oct 21, 2008"
    game.description = "This is a description"
    game.image_url = "https://example.com"
    game.website_url = "https://example.com"
    game.recommendations = 100
    game.windows = True
    game.mac = True
    game.linux = False
    game.categories = ['Action']
    game.achievements = 10
    game.developer = "Test Developer"
    game.screenshots = ["https://example.com"]
    game.movies = ["https://example.com"]

    user = User("Andrew", "Avocado101")
    user.wishlist.add_game(game)

    empty_session.add(user)
    empty_session.commit()

    # Test already exists for this
    game_id = list(empty_session.execute('SELECT game_id FROM games'))[0][0]

    # Test already exists for this
    user_id = list(empty_session.execute('SELECT id FROM users'))[0][0]

    # Check that the wishlists table has a new record
    rows = list(empty_session.execute('SELECT id, user_id FROM wishlists'))
    wishlist_id = rows[0][0]
    assert rows[0][1] == user_id

    # Check that the wishlist_games table has a new record
    rows = list(empty_session.execute('SELECT wishlist_id, game_id FROM wishlist_games'))
    assert rows == [
        (wishlist_id, game_id)
    ]
