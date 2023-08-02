"""
Movie Recommendation Application

This module contains a movie recommendation application implemented using Streamlit. The application allows users to
discover movie recommendations based on their preferences. It utilizes the OMDBApi for movie data retrieval and the
ContentBaseRecSys class for content-based movie recommendations.

The application interface is created with Streamlit, allowing users to select a movie they liked, specify their favorite
genres, actors, and country of production to receive personalized movie recommendations. The recommendations are
displayed alongside movie posters and additional movie information.

Modules:
    - os: Provides a way of using operating system-dependent functionality.
    - streamlit: Facilitates the creation of interactive web applications with simple Python scripts.
    - dotenv: Enables the reading of environment variables from a .env file.
    - api.omdb: Provides the OMDBApi class to fetch movie data from the OMDB API.
    - recsys: Contains the ContentBaseRecSys class responsible for content-based movie recommendations.
    - PIL: The Python Imaging Library used for image processing.
    - base64: Provides facilities for encoding binary data to base64 ASCII characters.

Functions:
    - initialize_data(): Loads environment variables, initializes the OMDBApi, and creates a ContentBaseRecSys instance.
    - get_all_actors(_recsys): Retrieves a sorted list of all actors from the ContentBaseRecSys instance.
    - get_base64_of_image(image_path): Converts an image file to a base64 encoded string.
    - main(): Entry point of the movie recommendation application. Sets up the Streamlit page, provides user input
        options, and displays movie recommendations based on user preferences.

Global Variables:
    - st.session_state.first_load (bool): Indicates whether it's the first load of the application.
    - st.session_state.last_index (int): Index of the last selected movie in the dropdown list.
    - st.session_state.translate (bool): Indicates whether movie overview translation is enabled.

Usage:
    Ensure the required environment variables (API_KEY, MOVIES, and DISTANCE) are set in a .env file before running
    the application. To start the application, run this script directly.
"""
import os
import streamlit as st
from dotenv import load_dotenv
from api.omdb import OMDBApi
from recsys import ContentBaseRecSys
from PIL import Image
import base64
import random


# Streamlit page configuration
st.set_page_config(page_title="School 21 - Data Science - Project 14  © D.Sha.", page_icon="assets/page_icon.png",
                   layout="wide", initial_sidebar_state="auto", menu_items=None)


@st.cache_data
def initialize_data():
    """
    Initialize data for the application.

    This function loads the API key, movies dataset file path, and distance file path from the environment variables,
    initializes the OMDB API with the API key, and creates an instance of ContentBaseRecSys for movie recommendations.

    Returns:
        Tuple[OMDBApi, ContentBaseRecSys]: A tuple containing the OMDBApi instance and ContentBaseRecSys instance.
    """
    load_dotenv()
    api_key = os.getenv("API_KEY")
    movies = os.getenv("MOVIES")
    distance = os.getenv("DISTANCE")
    omdb_api = OMDBApi(api_key)
    _recsys = ContentBaseRecSys(
        movies_dataset_filepath=movies,
        distance_filepath=distance,
    )
    return omdb_api, _recsys


@st.cache_data
def get_all_actors(_recsys):
    """
    Get All Actors from Content-Based Recommender

    This function retrieves a list of all actors from the ContentBaseRecSys instance.

    Args:
        _recsys (ContentBaseRecSys): The ContentBaseRecSys instance.

    Returns:
        List[str]: A list of all actor names.
    """
    all_actors = _recsys.get_all_actors()
    all_actors.insert(0, "")
    return all_actors


@st.cache_data
def get_base64_of_image(image_path):
    """
    Get Base64 Encoded Image Data

    This function reads the image data from the specified image file and converts it to base64 encoded format.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The base64 encoded image data.
    """
    with open(image_path, "rb") as img_file:
        img_data = base64.b64encode(img_file.read()).decode()
    return img_data


def main():
    """
    Main function to run the movie recommendation application using Streamlit.

    This function sets up the user interface, handles user inputs, and displays movie recommendations based on user
    preferences. It uses the ContentBaseRecSys class to provide personalized movie recommendations.

    User Interface:
    - The user can select a movie they like from a dropdown list.
    - The user can apply filters based on movie genres, actors, and countries of production using multiselect options.
    - After selecting a movie and applying filters, the user can click the "Показать рекомендации" button to view
      personalized movie recommendations.
    """
    top_k = 7
    page_title = "Сервис рекомендаций фильмов"
    welcome_text = "Откройте для себя свой новый любимый фильм!"
    service_info = """
    Сервис рекомендаций разработан, чтобы помочь вам найти идеальный фильм на основе ваших предпочтений.
    Просто выберите фильм, который вам понравился, и наш сервис предложит вам похожие фильмы, которые вам,
    возможно, тоже понравятся. Вы также можете настроить рекомендации, указав свой любимый жанр, страну производства
    фильма, режиссёра или актёра. Исследуйте мир персонализированных рекомендаций фильмов и откройте для себя
    следующее кинематографическое приключение!
    """
    copyright_text = "© 2023"
    st_button = True
    background_color = '#34C6CD'
    background_color2 = '#6C8AD5'
    text_color = '#006064'
    text_color2 = '#06246F'
    text_color3 = '#FFFFFF'

    image_path = os.path.join(os.getcwd(), "src/assets", "movietape1.jpg")
    encoded_image = get_base64_of_image(image_path)

    html_code = f"""
    <div style='background-color: white; padding: 16px; use_column_width="always"'>
        <div style='display: flex; justify-content: space-between; align-items: flex-end;
         background-color: {background_color};'>
            <h3 style='flex: 26; text-align: center; color: {text_color};
             font-family: "sans serif", Helvetica, Arial, sans-serif; font-size: 26px;'>{page_title}</h3>
            <p style='flex: 1; text-align: center; color: {text_color};'></p>
            <p style='flex: 66; text-align: center; color: {text_color3};'>{service_info}</p>
            <p style='flex: 1; text-align: center; color: {text_color};'></p>
            <img src="data:image/jpeg;base64,{encoded_image}" style='flex: 10; width: 150px; height: 150px;
             object-fit: cover;'>
        </div>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style='text-align: center; background-color: {background_color2}; color: {text_color2};'>
            <hr style='border-top: 1px solid {text_color2}; margin-top: 2px; margin-bottom: 5px;'/>
            <p style='margin: 0 auto;'>{welcome_text}</p>
            <hr style='border-top: 1px solid {text_color2}; margin-top: 2px; margin-bottom: 5px;'/>
        </div>
        """, unsafe_allow_html=True
    )

    col1, col2 = st.columns([25, 80])
    with col1:
        if st.session_state.first_load:
            random_index = random.randint(0, 4791)
            selected_movie = st.selectbox("Выберите фильм, который вам нравится:", recsys.get_title(),
                                          index=random_index)
            st.session_state.first_load = False
            st.session_state.last_index = random_index
        else:
            selected_movie = st.selectbox("Выберите фильм, который вам нравится:", recsys.get_title(),
                                          index=st.session_state.last_index)

        selected_genre = st.multiselect("Выберите жанры для фильтрации:", list(recsys.get_genres()))

        all_actors = get_all_actors(recsys)
        selected_actor = st.multiselect("Выберите актёра для фильтрации:", all_actors)

        selected_country = st.multiselect("Выберите страну:", list(recsys.get_country()))

        if st.button('Показать рекомендации'):
            st_button = True

        st.session_state.translate = st.checkbox('', value=True, help="переводить описание фильмов")

    with col2:
        st.markdown(
            """
            <style>
                .poster-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    text-align: center;
                }
        
                .poster-title {
                    font-size: 14px;
                    margin-top: 12px;
                    word-wrap: break-word;
                    text-align: center;
                    font-family: sans-serif, 'Arial';
                    color: #006064;
                }
        
                .poster-image {
                    width: 100%;
                    height: auto;
                }
            </style>
            """, unsafe_allow_html=True
        )

        if st_button:
            st.write("Рекомендуемые фильмы:")
            recommended_movie_names = recsys.recommendation(selected_movie, top_k=top_k, genres=selected_genre,
                                                            actor=selected_actor, country=selected_country)
            recommended_movie_posters = omdbapi.get_posters(recommended_movie_names)
            if recommended_movie_names:
                columns = st.columns(top_k)
                for index in range(min(len(recommended_movie_names), top_k)):
                    with columns[index]:
                        movie_url = recsys.get_movie_url(recommended_movie_names[index])
                        original_title = recsys.get_original_title(recommended_movie_names[index])
                        overview = recsys.get_overview(recommended_movie_names[index])
                        if st.session_state.translate:
                            if overview and overview.strip():
                                movie_overview = recsys.translate_to_russian(overview)
                            else:
                                movie_overview = overview
                        else:
                            movie_overview = overview
                        if movie_url:
                            st.markdown(
                                '<div class="poster-container">'
                                '<a href="{}" target="_blank">'
                                '<img class="poster-image" src="{}" title="{}"/>'
                                '<p class="poster-title" title="{}">{}</p>'
                                '</a>'
                                '</div>'.format(
                                    movie_url,
                                    recommended_movie_posters[index],
                                    movie_overview,
                                    original_title,
                                    recommended_movie_names[index]
                                ), unsafe_allow_html=True
                            )
                        else:
                            st.markdown(
                                '<div class="poster-container">'
                                '<img class="poster-image" src="{}" title="{}"/>'
                                '<p class="poster-title" title="{}">{}</p>'
                                '</div>'.format(
                                    recommended_movie_posters[index],
                                    movie_overview,
                                    original_title,
                                    recommended_movie_names[index]
                                ), unsafe_allow_html=True
                            )
            else:
                st.write("С заданными параметрами нет рекомендаций")

    st.markdown(
        f"""
        <div style='text-align: center; background-color: {background_color2}; color: {text_color2};'>
            <hr style='border-top: 1px solid {text_color2}; margin-top: 2px; margin-bottom: 5px;'/>
            <p style='margin: 0 auto;'>
            <a style='color: {text_color2};' href='https://github.com/dn0sh' target='_blank'>dn0sh</a>
            {copyright_text}</p>
            <hr style='border-top: 1px solid {text_color2}; margin-top: 2px; margin-bottom: 5px;'/>
        </div>
        """, unsafe_allow_html=True
    )

    image = Image.open("../assets/movietape2.jpg")
    st.image(image, use_column_width="always")


if __name__ == "__main__":
    if 'first_load' not in st.session_state:
        st.session_state.first_load = True
        st.session_state.last_index = None
        st.session_state.translate = False

    omdbapi, recsys = initialize_data()
    main()
