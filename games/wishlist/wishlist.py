from flask import Blueprint, redirect, url_for, request, render_template, session
from flask_wtf import FlaskForm

import games.adapters.repository as repo
from games.wishlist import services
from games.authentication.authentication import login_required

wishlist_blueprint = Blueprint(
    'wishlist_bp', __name__
)

@wishlist_blueprint.route('/wishlist', methods=['GET'])
@login_required
def wishlist():
    page = request.args.get('page', 1, type=int)

    user = repo.repo_instance.get_user(session['username'])
    wishlist = user.wishlist
    games, max_page = services.get_games_from_wishlist(wishlist, page)

    return render_template(
        'wishlist.html',
        games = games,
        page = page,
        max_page = max_page,
        num_games = len(wishlist.list_of_games()),
        username = user.username,
        form=FlaskForm,
    )

@wishlist_blueprint.route('/wishlist/remove/<int:game_id>', methods=['POST'])
@login_required
def remove_from_wishlist(game_id):
    if game_id:
        page = request.form.get('page', 1, type=int)
        user = repo.repo_instance.get_user(session['username'])
        game = repo.repo_instance.get_game(game_id)
        user.remove_from_wishlist(game)
        repo.repo_instance.add_user(user)
    return redirect(url_for('wishlist_bp.wishlist', page=page))