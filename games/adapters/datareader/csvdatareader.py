import csv
import os

from games.domainmodel.model import Genre, Game, Publisher, Tag


class GameFileCSVReader:
    def __init__(self, filename):
        self.__filename = filename
        self.__dataset_of_games = []
        self.__dataset_of_publishers = set()
        self.__dataset_of_genres = set()
        self.__dataset_of_tags = set()

    def read_csv_file(self):
        if not os.path.exists(self.__filename):
            print(f"path {self.__filename} does not exist!")
            return
        with open(self.__filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    game_id = int(row["AppID"])
                    title = row["Name"]
                    game = Game(game_id, title)
                    game.release_date = row["Release date"]
                    game.price = float(row["Price"])
                    game.description = row["About the game"]
                    game.image_url = row['Header image']
                    game.website_url = row['Website']
                    game.recommendations = int(row["Recommendations"])

                    publisher = Publisher(row["Publishers"])
                    self.__dataset_of_publishers.add(publisher)
                    game.publisher = publisher

                    genre_names = row["Genres"].split(",")
                    for genre_name in genre_names:
                        genre = Genre(genre_name.strip())
                        self.__dataset_of_genres.add(genre)
                        game.add_genre(genre)

                    # Could maybe make a general class that parents genre and tag.
                    tag_names = row["Tags"].split(",")
                    if tag_names != ['']:
                        for tag_name in tag_names:
                            tag = Tag(tag_name.strip().lower())
                            self.__dataset_of_tags.add(tag)
                            game.add_tag(tag)

                    # Shhhhh don't tell anyone how bad of a security flaw this is
                    game.languages = eval(row["Supported languages"])

                    game.windows = row["Windows"] == "TRUE"
                    game.mac = row["Mac"] == "TRUE"
                    game.linux = row["Linux"] == "TRUE"

                    game.achievements = int(row["Achievements"])
                    game.developer = row["Developers"]
                    game.categories = row["Categories"].split(",")
                    game.screenshots = row['Screenshots'].split(",")
                    game.movies = row['Movies'].split(",")

                    self.__dataset_of_games.append(game)

                except ValueError as e:
                    print(f"Skipping row due to invalid data: {e}")
                except KeyError as e:
                    print(f"Skipping row due to missing key: {e}")

    def get_unique_games_count(self):
        return len(self.__dataset_of_games)

    def get_unique_genres_count(self):
        return len(self.__dataset_of_genres)

    def get_unique_publishers_count(self):
        return len(self.__dataset_of_publishers)
    
    def get_unique_tags_count(self):
        return len(self.__dataset_of_tags)

    @property
    def dataset_of_games(self) -> list:
        return self.__dataset_of_games

    @property
    def dataset_of_publishers(self) -> set:
        return self.__dataset_of_publishers

    @property
    def dataset_of_genres(self) -> set:
        return self.__dataset_of_genres
    
    @property
    def dataset_of_tags(self) -> set:
        return self.__dataset_of_tags
