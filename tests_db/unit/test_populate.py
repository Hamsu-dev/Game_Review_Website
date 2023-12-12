from sqlalchemy import select, inspect

from games.adapters.orm import metadata

def test_db_table_names(database_engine):
    table_names = inspect(database_engine).get_table_names()
    for name in ['publishers', 'games', 'genres', 'game_genres', 'tags', 'game_tags', 'users', 'reviews', 'wishlists', 'wishlist_games']:
        assert name in table_names

def test_db_publishers(database_engine):
    with database_engine.connect() as con:
        results = con.execute( select([metadata.tables['publishers']]) )
        publishers = [r[0] for r in results.fetchall()]
        
        for publisher in ['rondomedia GmbH', 'Dahlenburg', 'Anvil-Soft,Plug In Digital', 'Klei Entertainment', 'Luden.io', 'Last Day Of Work', 'Xbox Game Studios', 'ToradySoft', 'Shaftesbury Sales Company', 'Schell Games', 'Stack Interactive', 'Dinosaur Polo Club', 'Activision', 'SCS Software', 'CJG Studio Ltd', 'Kiddy', 'Unknown', 'Antonio Renna', 'TechnoBrain', 'Azerbaijan Technology,Aztech']:
            assert publisher in publishers
    
def test_db_games(database_engine):
    with database_engine.connect() as con:
        results = con.execute( select([metadata.tables['games']]) )
        game_ids = [r[0] for r in results.fetchall()]

        for game in [
                7940,
                40800,
                457140,
                619150,
                270880,
                390220,
                1293830,
                1408380,
                1064920,
                1127500,
                358700,
                873970,
                350530,
                696760,
                910850,
                1348390,
                407420,
                1944970,
                618570,
                1053660
                ]:
            assert game in game_ids

def test_db_genres(database_engine):
    with database_engine.connect() as con:
        results = con.execute( select([metadata.tables['genres']]) )
        genres = [r[0] for r in results.fetchall()]

        for genre in ['Action', 'Indie', 'Simulation', 'Racing', 'Casual', 'Strategy', 'Adventure']:
            assert genre in genres

def test_db_tags(database_engine):
    with database_engine.connect() as con:
        results = con.execute( select([metadata.tables['tags']]) )
        tags = [r[0] for r in results.fetchall()]

        for tag in ['fps', 'action', 'multiplayer', 'shooter', 'singleplayer', 'first-person', 'classic', 'military', 'war', 'pvp', 'great soundtrack', 'linear', 'story rich', 'modern', 'co-op', 'atmospheric', 'controller', 'moddable', 'competitive', 'zombies', 'precision platformer', 'platformer', 'difficult', 'indie', '2d platformer', 'pixel graphics', '2d', 'fast-paced', 'retro', 'unforgiving', 'gore', 'time attack', 'funny', 'comedy', 'side scroller', 'replay value', 'colony sim', 'base-building', 'survival', 'resource management', 'building', 'management', 'simulation', 'sandbox', 'strategy', 'space', 'sci-fi', 'exploration', 'open world', 'adventure', 'early access', 'programming', 'education', 'puzzle', 'science', 'cats', 'investigation', 'underground', 'logic', 'transhumanism', 'dynamic narration', 'intentionally awkward controls', 'automobile sim', 'driving', 'transportation', 'america', 'realistic', 'relaxing', 'immersive sim', 'economy', 'casual', 'family friendly', 'level editor', 'psychological horror', 'racing', 'online co-op', 'arcade', 'sports', 'clicker', '3d', 'colorful', 'nonlinear', 'score attack', 'vr', 'minimalist', 'stylized', 'top-down', 'beautiful', 'city builder', 'physics', 'cartoony', 'fantasy', 'futuristic', 'choices matter', 'inventory management', 'flight', 'real time tactics', 'jet', 'tutorial', 'puzzle-platformer', 'rts', 'memes', 'parody', 'third person', 'third-person shooter', 'action-adventure', 'violent', 'mmorpg', 'action rpg', '3d platformer', 'combat racing', 'creature collector', 'dungeon crawler', 'medical sim', 'cute', 'vr only', 'fighting']:
            assert tag in tags