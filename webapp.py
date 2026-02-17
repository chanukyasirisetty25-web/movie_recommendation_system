import streamlit as st
import pandas as pd

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# ----------------------------
# POSTER WALLPAPER DESIGN
# ----------------------------
st.markdown("""
<style>

/* Poster Wallpaper Background */
.stApp {
    background-image: url("https://wallpapercave.com/wp/wp1817974.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Dark Overlay */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.85);
    z-index: -1;
}

/* Title */
.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: 2px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 20px;
    color: #cccccc;
    margin-bottom: 40px;
}

/* Glass Container */
.glass {
    background: rgba(255,255,255,0.07);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 0 30px rgba(0,0,0,0.6);
}

/* Dropdown */
div[data-baseweb="select"] > div {
    background-color: #1a1a1a !important;
    color: white !important;
    border-radius: 8px !important;
}

/* Button */
.stButton>button {
    background: linear-gradient(45deg, #ff0000, #b30000);
    color: white;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
    border-radius: 8px;
    width: 100%;
}

.stButton>button:hover {
    background: linear-gradient(45deg, #ff3333, #cc0000);
}

/* Movie Card */
.movie-card {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    transition: transform 0.3s ease;
}

.movie-card:hover {
    transform: scale(1.05);
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# SAMPLE MOVIE DATA
# ----------------------------
movies = pd.DataFrame({
    "title": [
        "Iron Man",
        "The Avengers",
        "Black Panther",
        "Thor",
        "Doctor Strange",
        "Captain Marvel",
        "Guardians of the Galaxy"
    ],
    "genre": [
        "Action", "Action", "Action",
        "Action", "Fantasy",
        "Action", "Adventure"
    ],
    "rating": [
        7.9, 8.0, 7.3,
        7.0, 7.5,
        6.8, 8.0
    ],
    "poster": [
        "https://image.tmdb.org/t/p/w500/78lPtwv72eTNqFW9COBYI0dWDJa.jpg",
        "https://image.tmdb.org/t/p/w500/RYMX2wcKCBAr24UyPD7xwmjaTn.jpg",
        "https://image.tmdb.org/t/p/w500/uxzzxijgPIY7slzFvMotPv8wjKA.jpg",
        "https://image.tmdb.org/t/p/w500/prSfAi1xGrhLQNxVSUFh61xQ4Qy.jpg",
        "https://image.tmdb.org/t/p/w500/uGBVj3bEbCoZbDjjl9wTxcygko1.jpg",
        "https://image.tmdb.org/t/p/w500/AtsgWhDnHTq68L0lLsUrCnM7TjG.jpg",
        "https://image.tmdb.org/t/p/w500/r7vmZjiyZw9rpJMQJdXpjgiCOk9.jpg"
    ]
})

# ----------------------------
# TITLE
# ----------------------------
st.markdown('<div class="main-title">MOVIE RECOMMENDATION SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find Your Next Favorite Movie</div>', unsafe_allow_html=True)

# ----------------------------
# MAIN GLASS CONTAINER
# ----------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

selected_movie = st.selectbox("🎥 Choose a Movie", movies["title"])

if st.button("🔥 Recommend Similar Movies"):

    selected_genre = movies[movies["title"] == selected_movie]["genre"].values[0]

    recommendations = movies[movies["genre"] == selected_genre]
    recommendations = recommendations[recommendations["title"] != selected_movie]

    st.markdown("## ⭐ Recommended Movies")

    cols = st.columns(len(recommendations))

    for i, (_, row) in enumerate(recommendations.iterrows()):
        with cols[i]:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
            st.image(row["poster"])
            st.markdown(f"**{row['title']}**")
            st.markdown(f"⭐ Rating: {row['rating']}")
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
