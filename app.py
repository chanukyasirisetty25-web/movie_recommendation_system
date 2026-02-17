import streamlit as st
import pandas as pd
import ast

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")

# ---------------- BACKGROUND DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1524985069026-dd778a71c7b4");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.stApp::before {
    content: "";
    position: fixed;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.85);
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
    height: 45px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA SAFELY ----------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("movies_metadata.csv", low_memory=False)
        df = df[['title', 'genres', 'vote_average', 'overview']]
        df = df.dropna()
        df = df.head(5000)  # limit for performance
        return df
    except:
        st.error("movies_metadata.csv file not found! Upload it in project folder.")
        st.stop()

movies = load_data()

# ---------------- PROCESS GENRES ----------------
def extract_genres(text):
    try:
        genres = ast.literal_eval(text)
        return [g['name'] for g in genres]
    except:
        return []

movies['genre_list'] = movies['genres'].apply(extract_genres)

# ---------------- TITLE ----------------
st.markdown('<div class="title">🎬 Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Discover Movies From All Genres</div>', unsafe_allow_html=True)

# ---------------- SELECT MOVIE ----------------
selected_movie = st.selectbox("Choose a Movie", movies['title'].values)

# ---------------- RECOMMEND FUNCTION ----------------
def recommend(movie):
    movie_genres = movies[movies['title'] == movie]['genre_list'].values[0]
    
    recommendations = []

    for index, row in movies.iterrows():
        if row['title'] != movie:
            common = set(movie_genres).intersection(set(row['genre_list']))
            score = len(common)
            if score > 0:
                recommendations.append((row['title'], row['vote_average'], score))
    
    recommendations = sorted(recommendations, key=lambda x: x[2], reverse=True)
    
    return recommendations[:10]

# ---------------- BUTTON ----------------
if st.button("🔥 Recommend Movies"):

    results = recommend(selected_movie)

    st.subheader("Top Recommendations:")

    for title, rating, score in results:
        st.write(f"🎥 **{title}**  | ⭐ Rating: {rating}")
