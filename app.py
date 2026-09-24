import os
import time
from io import BytesIO

import requests
import streamlit as st
import pandas as pd

from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# ENV
# ============================================================

load_dotenv()

TMDB_ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")


# ============================================================
# LOAD DATA
# ============================================================

try:

    movies = pd.read_csv(
        "dataset/movies_cleaned.csv"
    )

except FileNotFoundError:

    st.error(
        "dataset/movies_cleaned.csv not found."
    )

    st.stop()


movies["title"] = (
    movies["title"]
    .fillna("")
    .astype(str)
)

movies["tags"] = (
    movies["tags"]
    .fillna("")
    .astype(str)
)


# ============================================================
# BUILD MODEL
# ============================================================

@st.cache_resource
def build_model():

    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(
        movies["tags"]
    )

    similarity_matrix = cosine_similarity(
        tfidf_matrix
    )

    return (
        vectorizer,
        tfidf_matrix,
        similarity_matrix
    )


tfidf, tfidf_matrix, similarity = build_model()


# ============================================================
# MOVIE INDEX
# ============================================================

movie_indices = pd.Series(
    movies.index,
    index=movies["title"]
).drop_duplicates()


# ============================================================
# RECOMMENDATION FUNCTION
# ============================================================

def recommend(movie_title):

    if movie_title not in movie_indices:

        return []

    index = movie_indices[movie_title]

    similarity_scores = list(
        enumerate(
            similarity[index]
        )
    )

    similarity_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    top_movies = similarity_scores[1:6]

    recommendations = []

    for movie_index, score in top_movies:

        movie = movies.iloc[movie_index]

        recommendations.append(
            {
                "movie_id": int(
                    movie["movie_id"]
                ),
                "title": movie["title"],
                "score": float(score)
            }
        )

    return recommendations


# ============================================================
# TMDB REQUEST
# ============================================================

def tmdb_request(
    url,
    params=None
):

    if not TMDB_ACCESS_TOKEN:

        return None

    headers = {
        "Authorization":
            f"Bearer {TMDB_ACCESS_TOKEN}",
        "accept":
            "application/json"
    }

    for attempt in range(3):

        try:

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=15
            )

            if response.status_code == 200:

                return response.json()

            if response.status_code == 429:

                time.sleep(2)

                continue

            return None

        except requests.exceptions.RequestException:

            if attempt < 2:

                time.sleep(1)

    return None


# ============================================================
# TMDB MOVIE DETAILS
# ============================================================

@st.cache_data
def get_movie_details(
    movie_id,
    movie_title
):

    # --------------------------------------------------------
    # DIRECT MOVIE LOOKUP
    # --------------------------------------------------------

    url = (
        "https://api.themoviedb.org/3/movie/"
        f"{movie_id}"
    )

    data = tmdb_request(
        url,
        {
            "language": "en-US"
        }
    )


    # --------------------------------------------------------
    # FALLBACK SEARCH
    # --------------------------------------------------------

    if data is None:

        search_url = (
            "https://api.themoviedb.org/3/"
            "search/movie"
        )

        search_data = tmdb_request(
            search_url,
            {
                "query": movie_title,
                "language": "en-US",
                "page": 1,
                "include_adult": False
            }
        )

        if search_data is None:

            return None

        results = search_data.get(
            "results",
            []
        )

        if not results:

            return None

        data = results[0]


    # --------------------------------------------------------
    # POSTER URL
    # --------------------------------------------------------

    poster_path = data.get(
        "poster_path"
    )

    poster_url = None

    if poster_path:

        poster_url = (
            "https://image.tmdb.org/t/p/w500"
            + poster_path
        )


    return {
        "title":
            data.get(
                "title",
                movie_title
            ),

        "poster":
            poster_url,

        "rating":
            data.get(
                "vote_average",
                0
            ),

        "release_date":
            data.get(
                "release_date",
                ""
            ),

        "overview":
            data.get(
                "overview",
                ""
            )
    }


# ============================================================
# DOWNLOAD POSTER
# ============================================================

@st.cache_data
def download_poster(
    poster_url
):

    if not poster_url:

        return None

    try:

        response = requests.get(
            poster_url,
            timeout=15
        )

        if response.status_code == 200:

            return response.content

    except requests.exceptions.RequestException:

        pass

    return None


# ============================================================
# HERO
# ============================================================

st.write("")

st.caption(
    "✨ AI POWERED MOVIE DISCOVERY"
)

st.title(
    "🎬 CineMatch AI"
)

st.write(
    "Discover movies you'll love using "
    "Machine Learning, TF-IDF and Cosine Similarity."
)

st.write("")


# ============================================================
# SEARCH
# ============================================================

st.subheader(
    "🔎 Find your next movie"
)

st.caption(
    "Search for a movie and let CineMatch AI "
    "discover similar titles for you."
)


search_query = st.text_input(
    "Search",
    placeholder=(
        "Try Avatar, Batman, Titanic..."
    ),
    label_visibility="collapsed"
)


# ============================================================
# FILTER
# ============================================================

if search_query.strip():

    query = (
        search_query
        .strip()
        .lower()
    )

    filtered_movies = [

        title

        for title in movies["title"].tolist()

        if query in title.lower()
    ]

else:

    filtered_movies = (
        movies["title"].tolist()
    )


# ============================================================
# SELECT MOVIE
# ============================================================

if filtered_movies:

    selected_movie = st.selectbox(
        "🎥 Select a movie",
        filtered_movies
    )

else:

    selected_movie = None

    st.warning(
        "❌ No movie found. Try another name."
    )


# ============================================================
# BUTTON
# ============================================================

st.write("")

recommend_clicked = st.button(
    "🎯  Discover Similar Movies",
    use_container_width=True
)


# ============================================================
# RESULTS
# ============================================================

if recommend_clicked:

    if selected_movie is None:

        st.warning(
            "Please select a movie first."
        )

    else:

        recommendations = recommend(
            selected_movie
        )

        if not recommendations:

            st.warning(
                "No recommendations found."
            )

        else:

            st.write("")
            st.divider()
            st.write("")

            # ------------------------------------------------
            # RESULT HEADER
            # ------------------------------------------------

            st.caption(
                "✦ YOUR PERSONALIZED PICKS"
            )

            st.header(
                f"🎬 Movies similar to {selected_movie}"
            )

            st.caption(
                "Content-Based Filtering • "
                "TF-IDF • Cosine Similarity"
            )

            st.write("")


            # ------------------------------------------------
            # FIVE COLUMNS
            # ------------------------------------------------

            columns = st.columns(
                5,
                gap="medium"
            )


            # ------------------------------------------------
            # MOVIE CARDS
            # ------------------------------------------------

            for i, movie in enumerate(
                recommendations
            ):

                with columns[i]:

                    # ========================================
                    # CARD
                    # ========================================

                    with st.container(
                        border=True
                    ):

                        # ------------------------------------
                        # TMDB DETAILS
                        # ------------------------------------

                        details = get_movie_details(
                            movie["movie_id"],
                            movie["title"]
                        )


                        poster_bytes = None
                        rating = 0
                        release_date = ""
                        overview = ""


                        if details:

                            poster_url = details.get(
                                "poster"
                            )

                            poster_bytes = download_poster(
                                poster_url
                            )

                            rating = details.get(
                                "rating",
                                0
                            )

                            release_date = details.get(
                                "release_date",
                                ""
                            )

                            overview = details.get(
                                "overview",
                                ""
                            )


                        # ------------------------------------
                        # POSTER
                        # ------------------------------------

                        if poster_bytes:

                            st.image(
                                BytesIO(
                                    poster_bytes
                                ),
                                width="stretch"
                            )

                        else:

                            st.info(
                                "🎬 Poster unavailable"
                            )


                        # ------------------------------------
                        # RANK
                        # ------------------------------------

                        st.caption(
                            f"RECOMMENDATION #{i + 1}"
                        )


                        # ------------------------------------
                        # TITLE
                        # ------------------------------------

                        st.subheader(
                            movie["title"]
                        )


                        # ------------------------------------
                        # SIMILARITY
                        # ------------------------------------

                        similarity_percent = (
                            movie["score"] * 100
                        )

                        st.metric(
                            "🎯 Similarity",
                            f"{similarity_percent:.1f}%"
                        )


                        # ------------------------------------
                        # RATING
                        # ------------------------------------

                        if rating:

                            st.write(
                                f"⭐ {float(rating):.1f}/10"
                            )


                        # ------------------------------------
                        # YEAR
                        # ------------------------------------

                        if release_date:

                            st.write(
                                f"📅 {release_date[:4]}"
                            )


                        # ------------------------------------
                        # OVERVIEW
                        # ------------------------------------

                        if overview:

                            if len(overview) > 150:

                                overview = (
                                    overview[:150]
                                    + "..."
                                )

                            st.caption(
                                overview
                            )

                        else:

                            st.caption(
                                "No overview available."
                            )


            # ------------------------------------------------
            # HOW IT WORKS
            # ------------------------------------------------

            st.write("")
            st.divider()
            st.write("")

            st.caption(
                "🤖 BEHIND THE RECOMMENDATION"
            )

            st.subheader(
                "How CineMatch AI works"
            )

            st.write(
                "The system analyzes movie genres, "
                "keywords, plot overview, top cast "
                "and director. TF-IDF converts these "
                "features into numerical vectors, "
                "and Cosine Similarity finds movies "
                "with similar content."
            )


# ============================================================
# FOOTER
# ============================================================

st.write("")
st.divider()
st.write("")

footer1, footer2 = st.columns(2)

with footer1:

    st.caption(
        "🎬 CineMatch AI"
    )

with footer2:

    st.caption(
        "Python • Pandas • Scikit-learn • "
        "Streamlit • TMDB API"
    )

st.caption(
    "Content-Based Movie Recommendation System"
)