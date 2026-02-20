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
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("movies_small.csv")
    df = df[['title', 'genres', 'release_date']]
    df = df.dropna(subset=['genres'])
    return df

movies = load_data()

# -----------------------------
# EXTRACT GENRES
# -----------------------------
def extract_genres(genre_string):
    try:
        genres = ast.literal_eval(genre_string)
        return [g['name'] for g in genres]
    except:
        return []

movies['genre_list'] = movies['genres'].apply(extract_genres)

# -----------------------------
# UI
# -----------------------------
st.title("🎬 Movie Recommendation System")

genre_input = st.text_input("Enter Genre (Action, Comedy, Thriller etc.)")

if st.button("Show Movies"):
    if genre_input:

        filtered_movies = movies[movies['genre_list'].apply(
            lambda x: genre_input.lower() in [g.lower() for g in x]
        )]

        if not filtered_movies.empty:
            top_movies = filtered_movies.head(25)

            for index, row in top_movies.iterrows():
                year = ""
                if pd.notna(row['release_date']):
                    year = row['release_date'][:4]

                st.write(f"🎥 {row['title']} ({year})")

        else:
            st.warning("No movies found for this genre.")

    else:
        st.warning("Please enter a genre.")
