import streamlit as st
import pandas as pd
import ast

# --------------------------
# PAGE SETTINGS
# --------------------------
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# --------------------------
# DARK THEME STYLE
# --------------------------
st.markdown("""
<style>
.stApp {
    background-color: #0f0f0f;
    color: white;
}

.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #e50914;
}

.movie-box {
    background: #1c1c1c;
    padding: 15px;
    border-radius: 8px;
    margin: 8px 0;
    transition: 0.3s;
}

.movie-box:hover {
    background: #e50914;
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# LOAD DATA
# --------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("movies_metadata.csv", low_memory=False)
    df = df[['title', 'genres', 'release_date']]
    df = df.dropna(subset=['genres'])
    return df

movies = load_data()

# --------------------------
# FUNCTION TO EXTRACT GENRES
# --------------------------
def get_genre_list(genre_string):
    try:
        genres = ast.literal_eval(genre_string)
        return [g['name'] for g in genres]
    except:
        return []

movies['genre_list'] = movies['genres'].apply(get_genre_list)

# --------------------------
# UI
# --------------------------
st.markdown('<div class="title">🎬 Genre Based Movie Recommendation</div>', unsafe_allow_html=True)

genre_input = st.text_input("Enter Genre (Action, Comedy, Thriller, Drama etc.)")

if st.button("🍿 Get Movies"):
    if genre_input:

        filtered = movies[movies['genre_list'].apply(
            lambda x: genre_input.lower() in [g.lower() for g in x]
        )]

        if not filtered.empty:
            st.subheader(f"Top {min(25, len(filtered))} {genre_input.title()} Movies")

            top_movies = filtered.head(25)

            for i, row in top_movies.iterrows():
                year = ""
                if pd.notna(row['release_date']):
                    year = row['release_date'][:4]

                st.markdown(
                    f'<div class="movie-box">🎥 {row["title"]} ({year})</div>',
                    unsafe_allow_html=True
                )

        else:
            st.warning("No movies found for this genre.")

    else:
        st.warning("Please enter a genre.")

