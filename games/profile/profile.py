from flask import Blueprint, render_template, session, redirect, url_for
from flask_wtf import FlaskForm

import games.profile.services as services
from games.authentication.authentication import login_required
import games.adapters.repository as repo

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile')
@login_required
def profile():
    print(services.get_short_wishlist())
    return render_template(
        'profile.html',
        user = repo.repo_instance.get_user(session['username']),
        short_wishlist=services.get_short_wishlist(),
        empty_wishlist=True if len(services.get_short_wishlist()) == 0 else False,
        form=FlaskForm,
        )
