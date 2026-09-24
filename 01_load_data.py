import pandas as pd

movies = pd.read_csv("dataset/tmdb_5000_movies.csv")
credits = pd.read_csv("dataset/tmdb_5000_credits.csv")

print("Movies shape:", movies.shape)
print("Credits shape:", credits.shape)

print("\nMovies columns:")
print(movies.columns)

print("\nCredits columns:")
print(credits.columns)

print("\nFirst 5 movies:")
print(movies[["title", "genres", "keywords", "overview"]].head())

print("\nMissing values:")
print(movies[["title", "genres", "keywords", "overview"]].isnull().sum())

print("\nGenres example:")
print(movies["genres"].iloc[0])

print("\nKeywords example:")
print(movies["keywords"].iloc[0])

print("\nCast example:")
print(credits["cast"].iloc[0])

print("\nCrew example:")
print(credits["crew"].iloc[0])