import streamlit as st
import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("movies_small.csv", low_memory=False)
movies = movies[['title', 'genres']]
movies = movies.dropna()

def convert(text):
    try:
        genres_list = ast.literal_eval(text)
        return " ".join([i['name'] for i in genres_list])
    except:
        return ""

movies['genres'] = movies['genres'].apply(convert)

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['genres'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

movies = movies.reset_index(drop=True)

def recommend(title):
    idx = movies[movies['title'].str.lower() == title.lower()].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices]

st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a Movie:",
    movies['title'].values
)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    st.subheader("Top 5 Recommended Movies:")
    for movie in recommendations:
        st.write(movie)
