import os
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Configuration ---
# Adjust path if needed (e.g., if files are in a subfolder)
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
METADATA_PATH = os.path.join(DATA_DIR, "movies_metadata.csv")
SMALL_PATH = os.path.join(DATA_DIR, "movies_small.csv")

# Try movies_small first, fall back to movies_metadata
if os.path.exists(SMALL_PATH):
    df = pd.read_csv(SMALL_PATH)
elif os.path.exists(METADATA_PATH):
    df = pd.read_csv(METADATA_PATH)
else:
    raise FileNotFoundError("No movies CSV found: movies_small.csv or movies_metadata.csv")

# --- Genre mapping (for user input) ---
GENRE_MAPPING = {
    "action": "Action",
    "adventure": "Adventure",
    "comedy": "Comedy",
    "drama": "Drama",
    "thriller": "Thriller",
    "thriller/suspense": "Thriller",
    "romance": "Romance",
    "film noir": "Crime",
    "crime": "Crime",
    "musical": "Musical",
    "western": "Western",
    "animation": "Animation",
}

# --- Helper: parse genres from CSV ---
def parse_genres(genre_str):
    if pd.isna(genre_str):
        return []
    try:
        # If genres are stored as a JSON‑like string (common in movies_metadata.csv)
        import ast
        genres = ast.literal_eval(genre_str)
        return [g["name"] for g in genres]
    except:
        # Fallback: simple comma‑separated string
        return [g.strip() for g in str(genre_str).split(",") if g.strip()]


# --- Endpoint: home page ---
@app.route("/")
def index():
    return render_template("index.html")


# --- Endpoint: recommend by genre ---
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    genre_input = data.get("genre", "").strip().lower()

    # Map user input to internal genre
    mapped_genre = GENRE_MAPPING.get(genre_input)
    if not mapped_genre:
        return jsonify({
            "error": "Invalid genre. Please choose from: Action, Adventure, Comedy, Drama, Thriller, Romance, Crime, Musical, Western, Animation."
        })

    # Add parsed genres column if not present
    if "genres_parsed" not in df.columns:
        df["genres_parsed"] = df["genres"].apply(parse_genres)

    # Filter movies that contain the genre
    mask = df["genres_parsed"].apply(lambda gs: mapped_genre in gs)
    filtered = df[mask]

    # Ensure at least 50 movies; if not, pad with others (or reduce)
    titles = filtered["title"].dropna().tolist()
    if len(titles) < 50:
        # If dataset is small, pad with any movies (you can change logic)
        extra = df["title"].dropna().tolist()
        titles = (titles + extra)[:50]

    titles = titles[:50]  # Always return exactly 50

    return jsonify({
        "genre": mapped_genre,
        "movies": titles
    })


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)