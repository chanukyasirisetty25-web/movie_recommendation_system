import streamlit as st
import pandas as pd
import ast

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------
# CUSTOM DARK THEME CSS
# -----------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #141e30, #243b55);
    color: white;
}

.title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: #ff4b2b;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 40px;
    color: #dddddd;
}

.movie-card {
    background: #1e1e1e;
    padding: 15px;
    border-radius: 10px;
    margin: 8px 0;
    font-size: 17px;
    transition: 0.3s;
}

.movie-card:hover {
    background: #ff4b2b;
    transform: scale(1.02);
}

.stTextInput>div>div>input {
    background-color: #1e1e1e;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("movies_metadata.csv", low_memory=False)

    df = df[['title', 'genres', 'release_date']]
    df = df.dropna(subset=['genres'])

    return df

movies = load_data()

# -----------------------------
# EXTRACT GENRE FUNCTION
# -----------------------------
def extract_genres(genre_string):
    try:
        genres = ast.literal_eval(genre_string)
        return [g['name'] for g in genres]
    except:
        return []

movies['genre_list'] = movies['genres'].apply(extract_genres)

# -----------------------------
# UI SECTION
# -----------------------------
st.markdown('<div class="title">🎬 Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Get 25+ Movies Based on Your Favorite Genre</div>', unsafe_allow_html=True)

genre_input = st.text_input("🎥 Enter Genre (Action, Comedy, Thriller, Drama etc.)")

if st.button("🍿 Show Recommendations"):

    if genre_input:

        filtered_movies = movies[movies['genre_list'].apply(
            lambda x: genre_input.lower() in [g.lower() for g in x]
        )]

        if not filtered_movies.empty:

            st.subheader(f"Top {min(25, len(filtered_movies))} {genre_input.title()} Movies")

            top_25 = filtered_movies.head(25)

            for index, row in top_25.iterrows():

                year = ""
                if pd.notna(row['release_date']):
                    year = row['release_date'][:4]

                st.markdown(
                    f'<div class="movie-card">🎥 {row["title"]} ({year})</div>',
                    unsafe_allow_html=True
                )

        else:
            st.warning("No movies found for this genre.")

    else:
        st.warning("Please enter a genre.")
