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
# BACKGROUND DESIGN
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

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: white;
    margin-bottom: 5px;
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

.stButton>button:hover {
    background-color: #ff1e1e;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA SAFELY
# -----------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("movies_metadata.csv", low_memory=False)

        # Keep important columns
        df = df[['title', 'genres', 'vote_average', 'overview']]

        df = df.dropna()
        df = df.head(6000)  # Limit for performance

        return df

    except FileNotFoundError:
        st.error("❌ movies_metadata.csv not found! Upload it in your GitHub project.")
        st.stop()

movies = load_data()

# -----------------------------
# PROCESS GENRES
# -----------------------------
def extract_genres(text):
    try:
        genres = ast.literal_eval(text)
        return [g['name'] for g in genres]
    except:
        return []

movies['genre_list'] = movies['genres'].apply(extract_genres)

# -----------------------------
# TITLE SECTION
# -----------------------------
st.markdown('<div class="main-title">🎬 Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find Movies From Every Genre</div>', unsafe_allow_html=True)

# -----------------------------
# SELECT MOVIE
# -----------------------------
selected_movie = st.selectbox("🎥 Choose a Movie", movies['title'].values)

# -----------------------------
# RECOMMENDATION FUNCTION
# -----------------------------
def recommend(movie):
    movie_data = movies[movies['title'] == movie].iloc[0]
    movie_genres = movie_data['genre_list']

    recommendations = []

    for index, row in movies.iterrows():
        if row['title'] != movie:
            common_genres = set(movie_genres).intersection(set(row['genre_list']))
            score = len(common_genres)

            if score > 0:
                recommendations.append((
                    row['title'],
                    row['vote_average'],
                    score
                ))

    # Sort by similarity first, then rating
    recommendations = sorted(
        recommendations,
        key=lambda x: (x[2], x[1]),
        reverse=True
    )

    return recommendations[:10]

# -----------------------------
# BUTTON ACTION
# -----------------------------
if st.button("🔥 Recommend Movies"):

    results = recommend(selected_movie)

    st.subheader("⭐ Top Recommended Movies")

    if len(results) == 0:
        st.write("No similar movies found.")
    else:
        for title, rating, score in results:
            st.write(f"🎥 **{title}**  | ⭐ Rating: {rating}")

