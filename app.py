import pandas as pd

movies = pd.read_csv("movies_metadata.csv", low_memory=False)

# Keep only needed columns
movies = movies[['title', 'genres']]

# Remove missing values
movies = movies.dropna()

# Take only first 5000 rows
movies = movies.head(5000)

# Save smaller file
movies.to_csv("movies_small.csv", index=False)

print("Smaller dataset created successfully ✅")
