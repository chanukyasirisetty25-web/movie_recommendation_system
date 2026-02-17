import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------
# BACKGROUND STYLE
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.stApp::before {
    content: "";
    position: fixed;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.88);
    z-index: -1;
}

.title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    color: white;
}

.subtitle {
    text-align: center;
    color: #cccccc;
    margin-bottom: 40px;
}

.stButton>button {
    background-color: #e50914;
    color: white;
    font-size: 18px;
    height: 50px;
    border-radius: 8px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SMALL MOVIE DATASET
# -----------------------------
movies = pd.DataFrame({
    "title": [
        "Inception", "Titanic", "The Dark Knight",
        "Interstellar", "Avatar", "The Notebook",
        "The Conjuring", "Gladiator", "Joker",
        "Frozen", "Avengers: Endgame", "Parasite"
    ],
    "genre": [
        "Sci-Fi", "Romance", "Action",
        "Sci-Fi", "Sci-Fi", "Romance",
        "Horror", "Action", "Drama",
        "Animation", "Action", "Thriller"
    ],
    "rating": [
        8.8, 7.8, 9.0,
        8.6, 7.8, 7.9,
        7.5, 8.5, 8.4,
        7.4, 8.4, 8.6
    ]
})

# -----------------------------
# TITLE
# -----------------------------
st.markdown('<div class="title">🎬 Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Discover Movies From All Genres</div>', unsafe_allow_html=True)

# -----------------------------
# SELECT MOVIE
# -----------------------------
selected_movie = st.selectbox("Choose a Movie", movies["title"])

# -----------------------------
# RECOMMEND FUNCTION
# -----------------------------
def recommend(movie):
    selected_genre = movies[movies["title"] == movie]["genre"].values[0]
    recommendations = movies[movies["genre"] == selected_genre]
    recommendations = recommendations[recommendations["title"] != movie]
    return recommendations

# -----------------------------
# BUTTON
# -----------------------------
if st.button("🔥 Recommend Movies"):
    results = recommend(selected_movie)

    st.subheader("⭐ Recommended Movies")

    if results.empty:
        st.write("No similar movies found.")
    else:
        for index, row in results.iterrows():
            st.write(f"🎥 **{row['title']}** | ⭐ Rating: {row['rating']}")
