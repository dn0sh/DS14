import requests
from typing import Optional, List


class OMDBApi:
    """
    A simple Python wrapper for the OMDB API (Open Movie Database).

    Attributes:
        api_key (str): Your OMDB API key.
        url (str): The base URL of the OMDB API.

    Methods:
        _get_image_path(title: str) -> Optional[str]:
            Private method to fetch the image path (poster URL) for a given movie title.
        
        get_posters(titles: List[str]) -> List[str]:
            Fetches poster URLs for a list of movie titles.
            If the poster URL is not available, a placeholder loading image URL is provided.

    Usage Example:
        api_key = "YOUR_OMDB_API_KEY"
        omdb = OMDBApi(api_key)
        titles = ["Inception", "Interstellar", "The Dark Knight"]
        posters = omdb.get_posters(titles)
        print(posters)
    """

    def __init__(self, api_key: str):
        """
        Initialize the OMDBApi instance with your OMDB API key.

        :param api_key: Your OMDB API key.
        :type api_key: str
        """
        self.api_key = api_key
        self.url = "https://www.omdbapi.com"

    def _get_image_path(self, title: str) -> Optional[str]:
        """
        Private method to fetch the image path (poster URL) for a given movie title.

        :param title: The title of the movie.
        :type title: str
        :return: The poster URL if available, else None.
        :rtype: Optional[str]
        """
        params = {
            "apikey": self.api_key,
            "t": title,
            "type": "movie"
        }
        response = requests.get(self.url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'Poster' in data:
                return data['Poster']
        return None

    def get_posters(self, titles: List[str]) -> List[str]:
        """
        Fetches poster URLs for a list of movie titles.

        :param titles: A list of movie titles.
        :type titles: List[str]
        :return: A list of poster URLs corresponding to the given movie titles.
        :rtype: List[str]
        """
        posters = []
        for title in titles:
            path = self._get_image_path(title)
            if path:
                posters.append(path)
            else:
                posters.append('https://opros.pravovojstatus.ru/wp-content/plugins/Super-Quiz/admin/gifs/loading.gif')
        return posters
