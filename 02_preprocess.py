
import pandas as pd
import ast

# Load datasets
movies = pd.read_csv("dataset/tmdb_5000_movies.csv")
credits = pd.read_csv("dataset/tmdb_5000_credits.csv")

# Merge both datasets
movies = movies.merge(
    credits,
    left_on="id",
    right_on="movie_id"
)

print("Shape after merging:", movies.shape)

# Rename title_x
movies.rename(columns={"title_x": "title"}, inplace=True)

# Remove duplicate title column
movies.drop(columns=["title_y"], inplace=True)

# Convert JSON-like strings into Python lists
movies["genres"] = movies["genres"].apply(ast.literal_eval)
movies["keywords"] = movies["keywords"].apply(ast.literal_eval)
movies["cast"] = movies["cast"].apply(ast.literal_eval)
movies["crew"] = movies["crew"].apply(ast.literal_eval)


# Function to extract names
def convert_names(data):
    return [item["name"] for item in data]


# Extract names from genres and keywords
movies["genres"] = movies["genres"].apply(convert_names)
movies["keywords"] = movies["keywords"].apply(convert_names)


# Extract top 3 cast members
def get_top_cast(data):
    return [item["name"] for item in data[:3]]


movies["cast"] = movies["cast"].apply(get_top_cast)

# Extract director
def get_director(data):
    for item in data:
        if item["job"] == "Director":
            return item["name"]
    return ""


movies["director"] = movies["crew"].apply(get_director)

# Fill missing overview values
movies["overview"] = movies["overview"].fillna("")


# Convert lists into strings
movies["genres"] = movies["genres"].apply(lambda x: " ".join(x))
movies["keywords"] = movies["keywords"].apply(lambda x: " ".join(x))
movies["cast"] = movies["cast"].apply(lambda x: " ".join(x))


# Create tags column
movies["tags"] = (
    movies["genres"] + " "
    + movies["keywords"] + " "
    + movies["overview"] + " "
    + movies["cast"] + " "
    + movies["director"]
)


# Check tags
print("\nTags:")
print(movies["tags"].iloc[0])

print("\nDirector:")
print(movies["director"].iloc[0])

# Check the result
print("\nGenres:")
print(movies["genres"].iloc[0])

print("\nKeywords:")
print(movies["keywords"].iloc[0])

print("\nTop 3 Cast:")
print(movies["cast"].iloc[0])

# Keep only required columns
movies = movies[["movie_id", "title", "tags"]]

print("\nFinal dataset:")
print(movies.head())

print("\nFinal shape:")
print(movies.shape)

# Save preprocessed dataset
movies.to_csv("dataset/movies_cleaned.csv", index=False)

print("\nCleaned dataset saved successfully!")