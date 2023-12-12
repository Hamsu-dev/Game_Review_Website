import datetime


# Allows us to use wishlist for type hinting before it's defined.
class Wishlist:
    pass


class Publisher:
    def __init__(self, publisher_name: str):
        if publisher_name == "" or type(publisher_name) is not str:
            self.__publisher_name = None
        else:
            self.__publisher_name = publisher_name.strip()

    @property
    def publisher_name(self) -> str:
        return self.__publisher_name

    @publisher_name.setter
    def publisher_name(self, new_publisher_name: str):
        if new_publisher_name == "" or type(new_publisher_name) is not str:
            self.__publisher_name = None
        else:
            self.__publisher_name = new_publisher_name.strip()

    def __repr__(self):
        return f'<Publisher {self.__publisher_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.publisher_name == self.__publisher_name

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__publisher_name < other.publisher_name

    def __hash__(self):
        return hash(self.__publisher_name)


class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self) -> str:
        return f'<Genre {self.__genre_name}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.genre_name.lower() == self.__genre_name.lower()

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__genre_name < other.genre_name

    def __hash__(self):
        return hash(self.__genre_name)


class Tag:
    def __init__(self, tag_name: str):
        if tag_name == "" or type(tag_name) is not str:
            self.__tag_name = None
        else:
            self.__tag_name = tag_name.strip()

    @property
    def tag_name(self) -> str:
        return self.__tag_name

    def __repr__(self) -> str:
        return f'<Tag {self.__tag_name}>'
    
    def __str__(self) -> str:
        return self.__tag_name

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.__tag_name == self.__tag_name

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__tag_name < other.__tag_name

    def __hash__(self):
        return hash(self.__tag_name)


class Recommendations(int):
    def __str__(self):
        if self >= 20_000:
            return f'{self / 1000:.0f}k'
        elif self >= 1_000:
            return f'{self / 1000:.1f}k'
        else:
            return super().__str__()


class Game:
    def __init__(self, game_id: int, game_title: str):
        if type(game_id) is not int or game_id < 0:
            raise ValueError("Game ID should be a positive integer!")
        self.__game_id = game_id

        if type(game_title) is str and game_title.strip() != "":
            self.__game_title = game_title.strip()
        else:
            self.__game_title = None

        self.__price = None
        self.__release_date = None
        self.__description = None
        self.__image_url = None
        self.__website_url = None
        self.__genres: list = []
        self.__reviews: list = []
        self.__publisher = None
        self.__tags: list = []
        self.__recommendations = 0
        self.__languages: list = []
        self.__windows: bool = False
        self.__mac: bool = False
        self.__linux: bool = False
        self.__achievements: int = 0
        self.__developer: str = None
        self.__categories: list = []
        self.__screenshots: list = []
        self.__movies: list = []

    @property
    def publisher(self) -> Publisher:
        return self.__publisher

    @publisher.setter
    def publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher):
            self.__publisher = publisher
        else:
            self.__publisher = None

    @property
    def game_id(self):
        return self.__game_id

    @property
    def title(self):
        return self.__game_title

    @title.setter
    def title(self, new_title):
        if type(new_title) is str and new_title.strip() != "":
            self.__game_title = new_title.strip()
        else:
            self.__game_title = None

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price: float):
        if isinstance(price, (int, float)) and price >= 0:
            self.__price = price
        else:
            raise ValueError("Price must be a positive number!")

    @property
    def release_date(self):
        return self.__release_date

    @release_date.setter
    def release_date(self, release_date: str):
        if isinstance(release_date, str):
            try:
                # Check if the release_date string is in the correct date format (e.g., "Oct 21, 2008")
                datetime.datetime.strptime(release_date, "%b %d, %Y")
                self.__release_date = release_date
            except ValueError:
                raise ValueError("Release date must be in 'Oct 21, 2008' format!")
        else:
            raise ValueError("Release date must be a string in 'Oct 21, 2008' format!")

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description: str):
        if isinstance(description, str) and description.strip() != "":
            self.__description = description
        else:
            self.__description = None

    @property
    def image_url(self):
        return self.__image_url

    @image_url.setter
    def image_url(self, image_url: str):
        if isinstance(image_url, str) and image_url.strip() != "":
            self.__image_url = image_url
        else:
            self.__image_url = None

    @property
    def website_url(self):
        return self.__website_url

    @website_url.setter
    def website_url(self, website_url: str):
        if isinstance(website_url, str) and website_url.strip() != "":
            self.__website_url = website_url
        else:
            self.__website_url = None

    @property
    def reviews(self) -> list:
        return self.__reviews
    
    def add_review(self, new_review):
        if not isinstance(new_review, Review) or new_review in self.__reviews:
            return
        self.__reviews.append(new_review)

    def remove_review(self, review):
        if not isinstance(review, Review) or review not in self.__reviews:
            return
        self.__reviews.remove(review)

    @property
    def genres(self) -> list[Genre]:
        return self.__genres

    def add_genre(self, genre: Genre):
        if not isinstance(genre, Genre) or genre in self.__genres:
            return
        self.__genres.append(genre)

    def remove_genre(self, genre: Genre):
        if not isinstance(genre, Genre):
            return
        try:
            self.__genres.remove(genre)
        except ValueError:
            print(f"Could not find {genre} in list of genres.")
            pass
    
    @property
    def tags(self) -> list[Tag]:
        return self.__tags
    
    def add_tag(self, tag: Tag):
        if not isinstance(tag, Tag) or tag in self.__tags:
            return
        self.__tags.append(tag)
    
    def remove_tag(self, tag: Tag):
        if not isinstance(tag, Tag):
            return
        try:
            self.__tags.remove(tag)
        except ValueError:
            print(f"Could not find {tag} in list of tags.")
            pass
    
    @property
    def recommendations(self) -> float:
        return Recommendations(self.__recommendations)
    
    @recommendations.setter
    def recommendations(self, recommendations: int):
        if type(recommendations) is int and recommendations >= 0:
            self.__recommendations = recommendations

    @property
    def languages(self) -> list:
        return self.__languages
    
    @languages.setter
    def languages(self, languages: list):
        if isinstance(languages, list):
            self.__languages = languages

    @property
    def windows(self) -> bool:
        return self.__windows
    
    @windows.setter
    def windows(self, windows: bool):
        if isinstance(windows, bool):
            self.__windows = windows

    @property
    def mac(self) -> bool:
        return self.__mac
    
    @mac.setter
    def mac(self, mac: bool):
        if isinstance(mac, bool):
            self.__mac = mac

    @property
    def linux(self) -> bool:
        return self.__linux
    
    @linux.setter
    def linux(self, linux: bool):
        if isinstance(linux, bool):
            self.__linux = linux

    @property
    def achievements(self) -> int:
        return self.__achievements
    
    @achievements.setter
    def achievements(self, achievements: int):
        if isinstance(achievements, int) and 0 <= achievements:
            self.__achievements = achievements

    @property
    def developer(self) -> str: 
        return self.__developer
    
    @developer.setter
    def developer(self, developer: str):
        if isinstance(developer, str) and developer.strip() != "":
            self.__developer = developer.strip()
        else:
            self.__developer = None

    @property
    def categories(self) -> list:
        return self.__categories
    
    @categories.setter
    def categories(self, categories: list):
        if isinstance(categories, list):
            self.__categories = categories

    @property
    def screenshots(self) -> list:
        return self.__screenshots
    
    @screenshots.setter
    def screenshots(self, screenshots: list):
        if isinstance(screenshots, list):
            self.__screenshots = screenshots

    @property
    def movies(self) -> list:
        return self.__movies
    
    @movies.setter
    def movies(self, movies: list):
        if isinstance(movies, list):
            self.__movies = movies

    def __repr__(self):
        return f"<Game {self.__game_id}, {self.__game_title}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__game_id == other.__game_id

    def __hash__(self):
        return hash(self.__game_id)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__game_id < other.game_id


class User:
    def __init__(self, username: str, password: str):
        if not isinstance(username, str) or username.strip() == "":
            raise ValueError('Username cannot be empty or non-string!')
        else:
            self.__username = username.strip()

        if isinstance(password, str) and len(password) >= 7:
            self.__password = password
        else:
            raise ValueError('Password not valid!')

        self.__reviews: list[Review] = []
        self.__wishlist: Wishlist = Wishlist(self)

    @property
    def username(self):
        return self.__username

    @property
    def password(self) -> str:
        return self.__password

    @property
    def reviews(self) -> list:
        return self.__reviews

    def add_review(self, new_review):
        if not isinstance(new_review, Review) or new_review in self.__reviews:
            return
        self.__reviews.append(new_review)

    def remove_review(self, review):
        if not isinstance(review, Review) or review not in self.__reviews:
            return
        self.__reviews.remove(review)

    @property
    def wishlist(self) -> Wishlist:
        return self.__wishlist

    def add_to_wishlist(self, game):
        if not isinstance(game, Game) or game in self.__wishlist:
            return
        self.wishlist.add_game(game)

    def remove_from_wishlist(self, game):
        if not isinstance(game, Game) or game not in self.__wishlist:
            return
        self.__wishlist.remove_game(game)

    def __repr__(self):
        return f"<User {self.__username}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__username == other.username

    def __hash__(self):
        return hash(self.__username)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__username < other.username


class Review:
    def __init__(self, user: User, game: Game, rating: int, comment: str, date: datetime.date):

        if not isinstance(user, User):
            raise ValueError("User must be an instance of User class")
        self.__user = user

        if not isinstance(game, Game):
            raise ValueError("Game must be an instance of Game class")
        self.__game = game

        if not isinstance(rating, int) or not 0 <= rating <= 5:
            raise ValueError("Rating must be an integer between 0 and 5")
        self.__rating = rating

        if not isinstance(comment, str):
            raise ValueError("Comment must be a string")
        self.__comment = comment.strip()

        if not isinstance(date, datetime.date):
            raise ValueError("Date must be a datetime date object")
        self.__date = date

    @property
    def game(self) -> Game:
        return self.__game

    @property
    def comment(self) -> str:
        return self.__comment

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def user(self) -> User:
        return self.__user
    
    @property
    def date(self) -> datetime.date:
        return self.__date

    @comment.setter
    def comment(self, new_text):
        if isinstance(new_text, str):
            self.__comment = new_text.strip()
        else:
            raise ValueError("New comment must be a string")

    @rating.setter
    def rating(self, new_rating: int):
        if isinstance(new_rating, int) and 0 <= new_rating <= 5:
            self.__rating = new_rating
        else:
            raise ValueError("Rating must be an integer between 0 and 5")

    def __repr__(self):
        return f"Review(User: {self.__user}, Game: {self.__game}, " \
               f"Rating: {self.__rating}, Comment: {self.__comment})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.user == self.__user and other.game == self.__game and other.comment == self.__comment


class Wishlist:
    def __init__(self, user: User):
        if not isinstance(user, User):
            raise ValueError("User must be an instance of User class")
        self.__user = user
        self.__list_of_games = []

    def list_of_games(self):
        return self.__list_of_games

    def size(self):
        size_wishlist = len(self.__list_of_games)
        if size_wishlist > 0:
            return size_wishlist

    def add_game(self, game: Game):
        if isinstance(game, Game) and game not in self.__list_of_games:
            self.__list_of_games.append(game)

    def first_game_in_list(self):
        if len(self.__list_of_games) > 0:
            return self.__list_of_games[0]
        else:
            return None

    def remove_game(self, game):
        if isinstance(game, Game) and game in self.__list_of_games:
            self.__list_of_games.remove(game)

    def select_game(self, index):
        if 0 <= index < len(self.__list_of_games):
            return self.__list_of_games[index]
        else:
            return None

    def __iter__(self):
        self.__current = 0
        return self

    def __next__(self):
        if self.__current >= len(self.__list_of_games):
            raise StopIteration
        else:
            self.__current += 1
            return self.__list_of_games[self.__current - 1]
        
    def __repr__(self):
        return f"<Wishlist {self.__list_of_games}>"
    
    def __len__(self):
        return len(self.__list_of_games)
