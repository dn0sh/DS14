from typing import List, Set, Hashable
import pandas as pd
from .utils import parse
from googletrans import Translator


class ContentBaseRecSys:
    """
    Content-Based Movie Recommender System.

    This class implements a content-based recommender system that suggests movies based on the similarity of their
    content, such as genres, actors, and production countries.

    Attributes:
        distance (pd.DataFrame): A DataFrame representing the distance (similarity) between movies.
        movies (pd.DataFrame): A DataFrame containing movie data, including genres, actors, and production countries.

    Args:
        movies_dataset_filepath (str): The file path to the CSV file with movie data.
        distance_filepath (str): The file path to the CSV file with the distance matrix between movies.
    """

    def __init__(self, movies_dataset_filepath: str, distance_filepath: str):
        """
        Initialize the ContentBaseRecSys instance.

        Loads the distance matrix and movie data from the specified file paths.

        Args:
            movies_dataset_filepath (str): The file path to the CSV file with movie data.
            distance_filepath (str): The file path to the CSV file with the distance matrix between movies.
        """
        self.distance = pd.read_csv(distance_filepath, index_col='id')
        self.distance.index = self.distance.index.astype(int)
        self.distance.columns = self.distance.columns.astype(int)
        self._init_movies(movies_dataset_filepath)

    def _init_movies(self, movies_dataset_filepath) -> None:
        """
        Initialize movie data.

        Loads movie data from the specified CSV file and applies preprocessing, such as parsing genres.

        Args:
            movies_dataset_filepath (str): The file path to the CSV file with movie data.
        """
        self.movies = pd.read_csv(movies_dataset_filepath, index_col='id')
        self.movies.index = self.movies.index.astype(int)
        self.movies['genres'] = self.movies['genres'].apply(parse)

    def get_title(self) -> List[str]:
        """
        Get a list of movie titles.

        Returns:
            List[str]: A list of movie titles.
        """
        return self.movies['title'].values

    def get_genres(self) -> Set[str]:
        """
        Get a set of movie genres.

        Returns:
            Set[str]: A set containing all movie genres.
        """
        genres = [item for sublist in self.movies['genres'].values.tolist() for item in sublist]
        return set(genres)

    def get_country(self) -> Set[str]:
        """
        Get a set of production countries of movies.

        Returns:
            Set[str]: A set containing all production countries of movies.
        """
        country = self.movies['production_countries'].apply(lambda x: [country_i['name'] for country_i in eval(x)])
        country = [item for sublist in country.tolist() for item in sublist]
        return set(country)

    def recommendation(self, title: str, top_k: int = 5, genres: Set[str] = None,
                       actor: Set[str] = None, country: Set[str] = None) -> List[str]:
        """
        Get movie recommendations based on provided criteria.

        Recommends a list of movies similar to the provided movie title. Users can specify additional filters like
        genres, actors, and production countries.

        Args:
            title (str): The title of the movie for which recommendations are sought.
            top_k (int, optional): The number of top movie recommendations to return. Defaults to 5.
            genres (Set[str], optional): A set of movie genres for filtering the recommendations. Defaults to None.
            actor (Set[str], optional): A set of actors' names for filtering the recommendations. Defaults to None.
            country (Set[str], optional): A set of production countries for filtering the recommendations.
                Defaults to None.

        Returns:
            List[str]: A list of movie titles recommended based on the provided criteria.
        """
        movie_index = self.movies[self.movies['title'] == title].index[0]
        filtered_movies = self.filter_movies_by_genre_and_country(genres, country) if genres and country \
            else self.filter_movies_by_genre_and_actor(genres, actor) if genres and actor \
            else self.filter_movies_by_genre(genres) if genres \
            else self.filter_movies_by_actor(actor) if actor \
            else self.filter_movies_by_country(country) if country \
            else None

        top_movies_indices = self.get_top_k_movies(movie_index, top_k, filtered_movies, genres, actor, country)
        return self.movies.loc[top_movies_indices, 'title'].tolist()

    def get_top_k_movies(self, movie_index: int, top_k: int, filtered_movies: List[int] = None,
                         genres: Set[str] = None, actor: Set[str] = None, country: Set[str] = None) -> List[int]:
        """
        Get the top-k similar movies.

        Args:
            movie_index (int): The index of the movie for which recommendations are sought.
            top_k (int): The number of top movie recommendations to return.
            filtered_movies (List[int], optional): A list of movie indices to consider for recommendations.
            genres (Set[str], optional): A set of movie genres for filtering the recommendations.
            actor (Set[str], optional): A set of actors' names for filtering the recommendations.
            country (Set[str], optional): A set of production countries for filtering the recommendations.

        Returns:
            List[int]: A list of movie indices representing the top-k similar movies.
        """
        distances = self.distance.loc[movie_index].sort_values(ascending=False)
        if filtered_movies:
            distances = distances[distances.index.isin(filtered_movies)]
        if genres:
            filtered_indices = [index for index in distances.index if any(genre in self.movies.loc[index, 'genres']
                                                                          for genre in genres)]
            distances = distances[distances.index.isin(filtered_indices)]
        if actor:
            filtered_indices = [index for index in distances.index if any(person['name'] in actor for person
                                                                          in eval(self.movies.loc[index, 'cast']))]
            distances = distances[distances.index.isin(filtered_indices)]
        if country:
            filtered_indices = [index for index in distances.index
                                if any(country_i in self.movies.loc[index, 'production_countries']
                                       for country_i in country)]
            distances = distances[distances.index.isin(filtered_indices)]
        top_movies_indices = distances.index[1:top_k + 1]
        return top_movies_indices

    def update_recommendations(self, new_title: str, top_k: int = 5, genres: Set[str] = None,
                               actor: Set[str] = None, country: Set[str] = None) -> List[str]:
        return self.recommendation(new_title, top_k, genres, actor, country)

    def get_all_actors(self) -> List[str]:
        all_actors = set()
        for _, row in self.movies.iterrows():
            cast = eval(row['cast'])
            for person in cast:
                all_actors.add(person['name'].strip())
        return sorted(list(all_actors))

    def filter_movies_by_genre(self, genres: Set[str]) -> List[Hashable]:
        """
        Filter movies by genre.

        Args:
            genres (Set[str]): A set of movie genres for filtering.

        Returns:
            List[Hashable]: A list of movie indices representing the movies that match the provided genres.
        """
        filtered_movies = []
        for index, row in self.movies.iterrows():
            if any(genre in row['genres'] for genre in genres):
                filtered_movies.append(index)
        return filtered_movies

    def filter_movies_by_actor(self, actor: Set[str]) -> List[Hashable]:
        filtered_movies = []
        for index, row in self.movies.iterrows():
            cast = eval(row['cast'])
            if any(person['name'] in actor for person in cast):
                filtered_movies.append(index)
        return filtered_movies

    def filter_movies_by_genre_and_actor(self, genres: Set[str], actor: Set[str]) -> List[Hashable]:
        """
        Filter movies by genre and actor.

        Args:
            genres (Set[str]): A set of movie genres for filtering.
            actor (Set[str]): A set of actor names for filtering.

        Returns:
            List[Hashable]: A list of movie indices representing the movies that match the provided genres and include
            the provided actors.
        """
        filtered_movies = []
        for index, row in self.movies.iterrows():
            if any(genre in row['genres'] for genre in genres) or any(person['name'] in actor
                                                                      for person in eval(row['cast'])):
                filtered_movies.append(index)
        return filtered_movies

    def filter_movies_by_country(self, country: Set[str]) -> List[Hashable]:
        """
        Filter movies by production country.

        Args:
            country (Set[str]): A set of production countries for filtering.

        Returns:
            List[Hashable]: A list of movie indices representing the movies produced in the provided countries.
        """
        filtered_movies = []
        for index, row in self.movies.iterrows():
            if any(country_i in row['production_countries'] for country_i in country):
                filtered_movies.append(index)
        return filtered_movies

    def filter_movies_by_genre_and_country(self, genres: Set[str], country: Set[str]) -> List[Hashable]:
        """
        Filter movies by genre and production country.

        Args:
            genres (Set[str]): A set of movie genres for filtering.
            country (Set[str]): A set of production countries for filtering.

        Returns:
            List[Hashable]: A list of movie indices representing the movies that match the provided genres and were
            produced in the provided countries.
        """
        filtered_movies = []
        for index, row in self.movies.iterrows():
            if any(genre in row['genres'] for genre in genres) or any(country_i in row['production_countries']
                                                                      for country_i in country):
                filtered_movies.append(index)
        return filtered_movies

    def get_movie_url(self, movie_title: str) -> str:
        """
        Get the URL of a movie.

        Args:
            movie_title (str): The title of the movie.

        Returns:
            str: The URL of the movie or an empty string if the URL is not available.
        """
        movie_data = self.movies[self.movies['title'] == movie_title]
        movie_homepage = movie_data['homepage'].values[0] if not pd.isnull(movie_data['homepage'].values[0]) else None
        if movie_homepage:
            return movie_homepage
        else:
            return ''

    def get_original_title(self, movie_title: str) -> str:
        """
        Get the original title of a movie.

        Args:
            movie_title (str): The title of the movie.

        Returns:
            str: The original title of the movie or an empty string if the original title is not available.
        """
        try:
            original_title = self.movies.loc[self.movies['title'] == movie_title, 'original_title'].values[0]
            return original_title
        except IndexError:
            return ''

    def get_overview(self, movie_title: str) -> str:
        """
        Get the overview of a movie.

        Args:
            movie_title (str): The title of the movie.

        Returns:
            str: The overview of the movie or None if the overview is not available.
        """
        try:
            overview = self.movies.loc[self.movies['title'] == movie_title, 'overview'].values[0]
            return overview if not pd.isna(overview) else None
        except IndexError:
            return ''

    @staticmethod
    def translate_to_russian(text: str) -> str:
        """
        Translate text to Russian.

        Args:
            text (str): The text to be translated.

        Returns:
            str: The translated text in Russian.
        """
        translator = Translator()
        translated_text = translator.translate(text, src='en', dest='ru')
        return translated_text.text
