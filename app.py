import os
import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# ENVIRONMENT / DEPLOYMENT CONFIG
# ============================================================

def get_config(key, default=None):
    """
    Get configuration from Streamlit Secrets first,
    then environment variables, then default value.
    """

    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass

    return os.getenv(key, default)


API_BASE_URL = get_config(
    "API_BASE_URL",
    "https://movie-recommendation-system-burhan.onrender.com"
).rstrip("/")


# TMDB_API_KEY belongs to the FastAPI backend.
# Do NOT expose it in the Streamlit frontend.
#
# Local FastAPI:
# TMDB_API_KEY=your_key
#
# Deployed FastAPI:
# Add TMDB_API_KEY to backend environment/secrets.


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       GLOBAL
       ========================= */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(95, 75, 180, 0.16),
                transparent 28%
            ),
            radial-gradient(
                circle at 85% 15%,
                rgba(220, 60, 100, 0.10),
                transparent 28%
            ),
            #08080c;
        color: #f5f5f5;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* =========================
       HERO
       ========================= */

    div[data-testid="stHeading"] h1 {
        font-size: clamp(3rem, 7vw, 5.8rem);
        font-weight: 800;
        line-height: 0.98;
        letter-spacing: -3px;
    }

    .hero-caption {
        color: #9a9aa5;
        font-size: 1.05rem;
        line-height: 1.7;
        max-width: 720px;
        margin-bottom: 35px;
    }


    /* =========================
       SEARCH
       ========================= */

    div[data-testid="stTextInput"] input {
        background: #111116 !important;
        color: white !important;
        border: 1px solid #292934 !important;
        border-radius: 14px !important;
        padding: 16px !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #7165ff !important;
        box-shadow: 0 0 0 1px #7165ff !important;
    }


    /* =========================
       MOVIE IMAGES
       ========================= */

    div[data-testid="stImage"] img {
        border-radius: 12px;
    }


    /* =========================
       BUTTONS
       ========================= */

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid #292934;
        background: #15151c;
        color: white;
        font-weight: 600;
    }

    .stButton > button:hover {
        border-color: #7165ff;
        background: #1b1a27;
    }


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background: #0d0d12;
        border-right: 1px solid #1c1c24;
    }


    /* =========================
       DIVIDER
       ========================= */

    hr {
        border-color: #20202a;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# API HELPER
# ============================================================

def api_get(endpoint, params=None, timeout=30):
    """
    Send GET request to FastAPI backend.
    """

    url = f"{API_BASE_URL}{endpoint}"

    try:
        response = requests.get(
            url,
            params=params,
            timeout=timeout,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:
        st.error(
            f"Cannot connect to FastAPI backend.\n\n"
            f"Backend URL: {API_BASE_URL}"
        )
        return None

    except requests.exceptions.Timeout:
        st.error(
            "FastAPI backend took too long to respond."
        )
        return None

    except requests.exceptions.HTTPError as e:
        st.error(
            f"FastAPI returned an error: {e}"
        )
        return None

    except requests.exceptions.RequestException as e:
        st.error(
            f"Request failed: {e}"
        )
        return None


# ============================================================
# SESSION STATE
# ============================================================

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None

if "search_query" not in st.session_state:
    st.session_state.search_query = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## CineMatch")

    st.caption("Content-based movie discovery")

    st.divider()

    if st.button(
        "Home",
        use_container_width=True,
    ):
        st.session_state.selected_movie = None
        st.session_state.search_query = ""
        st.rerun()

    st.divider()

    st.markdown("### Recommendation Engine")

    st.caption(
        "TF-IDF converts movie metadata into numerical "
        "vectors. Cosine similarity finds movies with "
        "similar content."
    )

    st.divider()

    st.markdown("### Backend")

    st.code(API_BASE_URL)

    st.markdown("### Stack")

    st.caption(
        "Python\n"
        "FastAPI\n"
        "Streamlit\n"
        "TF-IDF\n"
        "Cosine Similarity\n"
        "TMDB"
    )


# ============================================================
# HERO
# ============================================================

st.title("Find your next favorite movie.")

st.caption(
    "Search for a movie and discover similar titles using "
    "a content-based recommendation engine powered by "
    "TF-IDF and cosine similarity."
)

st.write("")


# ============================================================
# SEARCH
# ============================================================

search_query = st.text_input(
    "Search",
    value=st.session_state.search_query,
    placeholder="Search for a movie...",
    label_visibility="collapsed",
)

st.session_state.search_query = search_query


# ============================================================
# SEARCH RESULTS
# ============================================================

if search_query.strip():

    results = api_get(
        "/tmdb/search",
        params={
            "query": search_query.strip(),
            "page": 1,
        },
    )

    if results:

        movies = results.get("results", [])

        if movies:

            st.subheader("Search results")

            st.caption(
                "Select a movie to generate recommendations."
            )

            st.write("")

            cols = st.columns(6)

            for i, movie in enumerate(movies[:12]):

                with cols[i % 6]:

                    poster_path = movie.get("poster_path")
                    title = movie.get("title") or "Unknown"

                    release_date = (
                        movie.get("release_date") or ""
                    )

                    if poster_path:

                        poster_url = (
                            "https://image.tmdb.org/t/p/w500"
                            + poster_path
                        )

                        st.image(
                            poster_url,
                            use_container_width=True,
                        )

                    else:

                        st.info("No poster")

                    st.markdown(f"**{title}**")

                    if release_date:
                        st.caption(release_date[:4])
                    else:
                        st.caption("Release year unavailable")

                    if st.button(
                        "Select",
                        key=f"search_movie_{movie.get('id')}",
                    ):
                        st.session_state.selected_movie = movie
                        st.rerun()

        else:

            st.info("No movies found.")


# ============================================================
# SELECTED MOVIE
# ============================================================

selected = st.session_state.selected_movie


if selected:

    selected_title = selected.get("title", "")

    bundle = api_get(
        "/movie/search",
        params={
            "query": selected_title,
            "tfidf_top_n": 12,
            "genre_limit": 12,
        },
        timeout=60,
    )

    if bundle:

        details = bundle.get("movie_details", {})

        title = (
            details.get("title")
            or selected_title
        )

        overview = (
            details.get("overview")
            or "No overview available."
        )

        poster_url = details.get("poster_url")

        release_date = (
            details.get("release_date")
            or ""
        )

        genres = details.get("genres") or []


        # ====================================================
        # SELECTED MOVIE
        # ====================================================

        st.divider()

        st.subheader("Selected movie")

        left, right = st.columns(
            [1, 2.5],
            gap="large",
        )

        with left:

            if poster_url:

                st.image(
                    poster_url,
                    use_container_width=True,
                )

            else:

                st.info("No poster available.")


        with right:

            st.markdown(f"## {title}")

            if release_date:

                st.caption(
                    f"Release year: {release_date[:4]}"
                )

            st.write("")

            st.write(overview)

            st.write("")

            if genres:

                st.markdown("**Genres**")

                genre_names = [
                    genre.get("name")
                    for genre in genres
                    if genre.get("name")
                ]

                if genre_names:

                    st.write(
                        " • ".join(genre_names)
                    )


        # ====================================================
        # TF-IDF RECOMMENDATIONS
        # ====================================================

        st.divider()

        st.subheader(
            "Because you watched this"
        )

        st.caption(
            "Recommendations generated using "
            "TF-IDF and cosine similarity."
        )

        tfidf_recs = bundle.get(
            "tfidf_recommendations",
            [],
        )

        if tfidf_recs:

            cols = st.columns(6)

            for i, rec in enumerate(
                tfidf_recs[:12]
            ):

                with cols[i % 6]:

                    tmdb = rec.get("tmdb") or {}

                    poster = tmdb.get(
                        "poster_url"
                    )

                    rec_title = (
                        rec.get("title")
                        or "Unknown"
                    )

                    score = rec.get(
                        "score",
                        0,
                    )

                    if poster:

                        st.image(
                            poster,
                            use_container_width=True,
                        )

                    else:

                        st.info("No poster")

                    st.markdown(
                        f"**{rec_title}**"
                    )

                    st.caption(
                        f"Similarity: "
                        f"{float(score):.3f}"
                    )

        else:

            st.info(
                "No local TF-IDF recommendations "
                "were found."
            )


        # ====================================================
        # GENRE RECOMMENDATIONS
        # ====================================================

        st.divider()

        st.subheader("More like this")

        st.caption(
            "Popular movies from the same genre."
        )

        genre_recs = bundle.get(
            "genre_recommendations",
            [],
        )

        if genre_recs:

            cols = st.columns(6)

            for i, movie in enumerate(
                genre_recs[:12]
            ):

                with cols[i % 6]:

                    poster = movie.get(
                        "poster_url"
                    )

                    movie_title = (
                        movie.get("title")
                        or "Unknown"
                    )

                    rating = movie.get(
                        "vote_average"
                    )

                    if poster:

                        st.image(
                            poster,
                            use_container_width=True,
                        )

                    else:

                        st.info("No poster")

                    st.markdown(
                        f"**{movie_title}**"
                    )

                    if rating is not None:

                        st.caption(
                            f"Rating: "
                            f"{float(rating):.1f}/10"
                        )

        else:

            st.info(
                "No genre recommendations "
                "available."
            )


# ============================================================
# HOME FEED
# ============================================================

else:

    st.divider()

    st.subheader("Popular right now")

    st.caption(
        "Currently popular movies from TMDB."
    )

    st.write("")

    home_movies = api_get(
        "/home",
        params={
            "category": "popular",
            "limit": 18,
        },
        timeout=30,
    )

    if home_movies:

        cols = st.columns(6)

        for i, movie in enumerate(
            home_movies
        ):

            with cols[i % 6]:

                poster = movie.get(
                    "poster_url"
                )

                title = (
                    movie.get("title")
                    or "Unknown"
                )

                rating = movie.get(
                    "vote_average"
                )

                if poster:

                    st.image(
                        poster,
                        use_container_width=True,
                    )

                else:

                    st.info("No poster")

                st.markdown(
                    f"**{title}**"
                )

                if rating is not None:

                    st.caption(
                        f"Rating: "
                        f"{float(rating):.1f}/10"
                    )

    else:

        st.warning(
            "Unable to load movies. "
            "Make sure FastAPI is running."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CineMatch · Built with Python, FastAPI, "
    "Streamlit, TF-IDF and TMDB"
)
