from flask import render_template, Blueprint, redirect, url_for, request
from bisect import insort_left
from math import ceil

import games.adapters.repository as repo
from games.browse import services


browse_blueprint = Blueprint(
    'games_bp', __name__
)

@browse_blueprint.route('/browse', methods=['GET', 'POST'])
def browse_games():
    search_string = request.args.get('search', None, type=str)
    genre = services.get_genre_from_request(request)
    page = request.args.get('page', 1, type=int)
    games, num_games = services.search_games(repo.repo_instance, page=page, title=search_string, genre=genre)
    return _browse_games_render(games=games, cur_search=search_string, cur_genre=genre, num_games=num_games, page=page)

@browse_blueprint.route('/browse/', methods=['GET', 'POST'])
def browse_games_with_slash():
    search_string = request.args.get('search', None, type=str)
    if not search_string:
        search_string = request.form.get('search', None, type=str)
    genre = services.get_genre_from_request(request)
    page = request.args.get('page', 1, type=int)
    return redirect(url_for('games_bp.browse_games', search=search_string, genre=genre, page=page))

@browse_blueprint.route('/browse/<path:subpath>', methods=['GET', 'POST'])
def browse_games_with_options(subpath: str):

    subpath, tag_path, sort, tags, bad_url = services.parse_subpath(subpath, repo.repo_instance)

    from_form = False
    search_string = request.args.get('search', None, type=str)
    if not search_string:
        search_string = request.form.get('search', None, type=str)
        if search_string:
            from_form = True # This is a little bit hacky.
        # The problem is that if the form sends a GET request then the form data replaces the query string. We need both the query string and the form data, so this is what we got.
    genre = services.get_genre_from_request(request)
    page = request.args.get('page', 1, type=int)

    if bad_url or from_form: # Redirect to correct url
        return redirect(url_for('games_bp.browse_games_with_options', subpath=subpath, search=search_string, genre=genre, page=page))

    games, num_games = services.search_games(repo.repo_instance, title=search_string, tags=tags, genre=genre, page=page, sort=sort)

    return _browse_games_render(
            cur_sort = sort,
            cur_tags = tags,
            cur_subpath = subpath,
            cur_tag_path = tag_path,
            cur_search = search_string,
            cur_genre = genre,
            games = games,
            page=page,
            num_games=num_games)

def _browse_games_render(
        cur_sort = '',
        cur_tags = [],
        cur_subpath = '',
        cur_tag_path = '',
        cur_search = None,
        cur_genre = None,
        games = [],
        page = 1,
        num_games = 0):
    random_tags = services.get_random_tags(repo.repo_instance, 5)
    random_genres = services.get_random_genres(repo.repo_instance, 5)
    return render_template(
        'browse.html',
        # Custom page title
        title = f"Browse Games | CS235 Game Library",
        # Page heading
        heading = "Browse Games",

        # Search Options
        cur_sort = cur_sort,
        cur_tags = cur_tags,
        cur_search = cur_search,
        cur_genre = cur_genre,
        # Page URL
        cur_subpath = cur_subpath,
        cur_tag_path = cur_tag_path,
        
        # Tags
        random_tags = random_tags,
        all_tags = sorted(repo.repo_instance.get_tags()),

        # Genres
        random_genres = random_genres,
        all_genres = services.get_all_genres(repo.repo_instance),

        # Search Results
        games = games,
        num_games = num_games,

        # Pagination
        page = page,
        max_page = ceil(num_games/services.GAMES_PER_PAGE)
    )

@browse_blueprint.route('/add_tags', methods=['POST'])
def add_tags():
    # Read form data
    form_tags = []
    for key, value in request.form.items():
        if key == 'tag-dropdown' and value != 'null-selection':
            insort_left(form_tags, value)
        else:
            insort_left(form_tags, value)

    subpath = request.args.get('subpath', '', type=str)
    for tag in form_tags:
        subpath += '/' + tag

    search_string = request.args.get('search', None, type=str)
    page = request.args.get('page', 1, type=int)
    genre = services.get_genre_from_request(request)

    return redirect(url_for('games_bp.browse_games_with_options', subpath=subpath, search=search_string, page=page, genre=genre))

@browse_blueprint.route('/set_genre', methods=['GET'])
def set_genre():
    genre = services.get_genre_from_request(request)
    search_string = request.args.get('search', None, type=str)
    page = request.args.get('page', None, type=int)
    subpath = request.args.get('subpath', '', type=str)
    return redirect(url_for('games_bp.browse_games_with_options', subpath=subpath, search=search_string, genre=genre, page=page))