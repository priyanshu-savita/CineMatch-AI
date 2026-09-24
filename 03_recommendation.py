
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# 1. Load cleaned dataset
# ==========================================

movies = pd.read_csv("dataset/movies_cleaned.csv")

print("Dataset shape:", movies.shape)


# ==========================================
# 2. Create TF-IDF Vectorizer
# ==========================================

tfidf = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)


# ==========================================
# 3. Convert movie tags into TF-IDF vectors
# ==========================================

tfidf_matrix = tfidf.fit_transform(movies["tags"])

print("\nTF-IDF matrix shape:")
print(tfidf_matrix.shape)


# ==========================================
# 4. Calculate Cosine Similarity
# ==========================================

similarity = cosine_similarity(tfidf_matrix)

print("\nSimilarity matrix shape:")
print(similarity.shape)


# ==========================================
# 5. Create movie index
# ==========================================

movie_indices = pd.Series(
    movies.index,
    index=movies["title"]
).drop_duplicates()


# ==========================================
# 6. Recommendation Function
# ==========================================

def recommend(movie_title):

    # Check whether movie exists
    if movie_title not in movie_indices:
        print(f"\nMovie '{movie_title}' not found.")
        return

    # Get movie index
    index = movie_indices[movie_title]

    # Get similarity scores
    similarity_scores = list(
        enumerate(similarity[index])
    )

    # Sort by similarity score
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Get top 5 similar movies
    top_movies = similarity_scores[1:6]

    print(f"\nMovies similar to '{movie_title}':")

    for movie_index, score in top_movies:

        movie_name = movies.iloc[movie_index]["title"]

        print(
            movie_name,
            "->",
            round(score, 3)
        )


# ==========================================
# 7. Test Recommendation
# ==========================================

recommend("Avatar")

