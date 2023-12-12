"""Initialize Flask app."""

from pathlib import Path
from flask import Flask, render_template

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import clear_mappers, sessionmaker
from sqlalchemy.pool import NullPool

import games.adapters.repository as repo
import games.adapters.memory_repository as memory_repository
import games.adapters.database_repository as database_repository
from games.adapters.orm import metadata, map_model_to_tables

import os
from werkzeug.security import generate_password_hash
from games.domainmodel.model import User
from games.adapters.repository import AbstractRepository

def initialize_admin_account(repo: AbstractRepository):
    admin_username = "Sam"
    admin_password = "Test12345"

    if not repo.get_user(admin_username):
        password_hash = generate_password_hash(admin_password)
        admin_user = User(admin_username, password_hash)
        repo.add_user(admin_user)
        print("Admin account created successfully.")


def create_app(test_config=None):
    """Construct the core application."""
    print("Creating the Flask app...")
    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Switch the type of repository used depending on the env variables
    if app.config['REPOSITORY'] == 'memory':    
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = memory_repository.MemoryRepository()

        # fill the repository from the provided csv file.
        memory_repository.populate(data_path, repo.repo_instance)

    elif app.config['REPOSITORY'] == 'database':
        uri = app.config['SQLALCHEMY_DATABASE_URI']
        echo = app.config['SQLALCHEMY_ECHO']

        database_engine = create_engine(uri, echo=echo,
            connect_args={"check_same_thread": False}, poolclass=NullPool
        )

        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = database_repository.DatabaseRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            # Initialize the database if needed
            print("INFO: REPOPULATING DATABASE...")

            clear_mappers()
            metadata.create_all(database_engine)
            for table in reversed(metadata.sorted_tables):
                database_engine.execute(table.delete())

            map_model_to_tables()

            database_repository.populate(data_path, repo.repo_instance)
            print("INFO: REPOPULATION COMPLETE")
        else:
            # Generate mappings
            map_model_to_tables()

    # Initialize the admin account
    initialize_admin_account(repo.repo_instance)

    with app.app_context():
        # Register the blueprints to the app instance.
        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)

        from .game import game
        app.register_blueprint(game.game_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .wishlist import wishlist
        app.register_blueprint(wishlist.wishlist_blueprint)

        from games.profile.profile import profile_bp
        app.register_blueprint(profile_bp)

        # Register a callback the makes sure that database sessions are associated with http requests
        # We reset the session inside the database repository before a new flask request is generated
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.DatabaseRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.DatabaseRepository):
                repo.repo_instance.close_session()

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.context_processor
    def generate_star_rating():
        def star_rating(rating):
            # There's no half star unicode character :(
            # return 'star ' * math.floor(rating) + 'star-half ' * (math.floor(rating) != math.ceil(rating)) + 'star-empty ' * (5 - math.ceil(rating))
            return '★' * int(rating + 0.5) + '☆' * (5 - int(rating + 0.5))
        return dict(star_rating=star_rating)

    @app.context_processor
    def inject_genres():
        genres = repo.repo_instance.get_genres()
        return dict(all_genres = [g.genre_name for g in genres])

    @app.route('/')
    def home():
        # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
        return render_template('main.html', heading="Discover new games")
    

    return app
