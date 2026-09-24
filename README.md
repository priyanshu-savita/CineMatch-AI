# 🎬 CineMatch AI — Movie Recommendation System

CineMatch AI is a **Content-Based Movie Recommendation System** that uses Machine Learning and Natural Language Processing techniques to recommend movies similar to a movie selected by the user.

The system analyzes movie **genres, keywords, plot overview, top cast members, and director information**, converts this information into numerical vectors using **TF-IDF**, and calculates movie similarity using **Cosine Similarity**.

A Streamlit web application provides an interactive interface where users can search for a movie and discover five similar movies along with posters, ratings, release years, similarity scores, and descriptions.

---

## ✨ Features

* 🎬 Content-based movie recommendations
* 🔎 Movie search and filtering
* 🤖 TF-IDF based feature extraction
* 📐 Cosine Similarity based recommendations
* 🎯 Top 5 similar movies
* 🖼️ Movie posters using TMDB API
* ⭐ TMDB movie ratings
* 📅 Release year
* 📝 Movie overview
* ⚡ Streamlit web interface
* 🚀 Cached ML model and API responses
* 🔐 Environment variable support for API credentials

---

## 🧠 Machine Learning Approach

CineMatch AI uses a **Content-Based Filtering** approach.

The recommendation pipeline is:

```text
TMDB 5000 Dataset
        ↓
Data Cleaning
        ↓
Merge Movies + Credits
        ↓
Feature Extraction
        ↓
Genres + Keywords + Overview
+ Top 3 Cast + Director
        ↓
Create Movie Tags
        ↓
TF-IDF Vectorization
        ↓
Cosine Similarity
        ↓
Find Most Similar Movies
        ↓
Top 5 Recommendations
```

---

## 📊 Dataset

The project uses the **TMDB 5000 Movie Dataset** containing approximately **4,800 movies**.

Two datasets are used:

* `tmdb_5000_movies.csv`
* `tmdb_5000_credits.csv`

After preprocessing, the final dataset contains:

```text
4803 movies
3 columns
```

Final columns:

```text
movie_id
title
tags
```

---

## 🔧 Data Preprocessing

The raw dataset contains JSON-like information for genres, keywords, cast, and crew.

The preprocessing pipeline performs:

1. Merge movie and credits datasets
2. Parse JSON-like strings using `ast.literal_eval`
3. Extract genre names
4. Extract keyword names
5. Extract top 3 cast members
6. Extract movie director
7. Handle missing movie overviews
8. Convert feature lists into text
9. Combine features into a single `tags` column
10. Save the cleaned dataset

Example:

```text
Genres
+
Keywords
+
Overview
+
Top Cast
+
Director
        ↓
Movie Tags
```

---

## 🧮 TF-IDF Vectorization

TF-IDF stands for **Term Frequency–Inverse Document Frequency**.

It converts the text-based movie tags into numerical vectors.

The project uses:

```python
TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)
```

The resulting TF-IDF matrix contains:

```text
4803 movies × 5000 features
```

---

## 📐 Cosine Similarity

After converting movies into TF-IDF vectors, the system calculates the similarity between movies using **Cosine Similarity**.

The similarity matrix contains:

```text
4803 × 4803
```

Each value represents how similar two movies are based on their textual features.

---

## 🎯 Example Recommendation

For the movie:

```text
Avatar
```

The current model produces:

```text
Aliens                         43.0%
Alien                          36.3%
Moonraker                      34.9%
Alien³                         34.7%
Silent Running                 31.5%
```

For:

```text
Iron Man
```

Example results:

```text
Iron Man 2                    56.6%
Iron Man 3                    54.3%
Avengers: Age of Ultron       43.7%
Captain America: Civil War    35.8%
The Incredible Hulk           34.4%
```

---

## 🌐 Web Application

The project uses **Streamlit** to provide an interactive web interface.

Users can:

1. Search for a movie
2. Select a movie
3. Click **Discover Similar Movies**
4. View five recommended movies
5. See similarity percentage
6. See TMDB rating
7. See release year
8. Read the movie overview
9. View movie posters

---

## 🎥 TMDB API Integration

The application uses the **TMDB API** to retrieve additional movie information such as:

* Movie poster
* Rating
* Release date
* Overview

The API token is stored securely in an environment file:

```text
.env
```

Example:

```text
TMDB_ACCESS_TOKEN=your_token_here
```

> Never upload your real API token to GitHub.

---

## 🛠️ Technologies Used

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Core programming language       |
| Pandas        | Data loading and preprocessing  |
| NumPy         | Numerical computation           |
| Scikit-learn  | TF-IDF and Cosine Similarity    |
| Streamlit     | Web application                 |
| Requests      | TMDB API requests               |
| Python-dotenv | Environment variable management |
| TMDB API      | Movie metadata and posters      |

---

## 📁 Project Structure

```text
movie-recommendation-system/
│
├── .venv/
│
├── dataset/
│   ├── tmdb_5000_movies.csv
│   ├── tmdb_5000_credits.csv
│   └── movies_cleaned.csv
│
├── 01_load_data.py
├── 02_preprocess.py
├── 03_recommendation.py
│
├── app.py
│
├── app_backup.py
├── app_working_backup.py
├── app_premium_backup.py
│
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
```

### 2. Open the project

```bash
cd movie-recommendation-system
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\activate
```

### 5. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 🔑 Configure TMDB API

Create a `.env` file in the project root:

```text
TMDB_ACCESS_TOKEN=your_tmdb_access_token
```

Replace the value with your TMDB API access token.

---

## ▶️ Run the Project

Start the Streamlit application:

```powershell
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

---

## 🧪 Testing

The recommendation model has been tested with multiple movies including:

* Avatar
* The Dark Knight
* Titanic
* Iron Man
* The Avengers

The system successfully generated five recommendations for each tested movie.

---

## 📈 Model Information

```text
Dataset Size:
4803 movies

TF-IDF Features:
5000

TF-IDF Matrix:
4803 × 5000

Similarity Matrix:
4803 × 4803

Recommendation Type:
Content-Based Filtering

Recommendations:
Top 5 similar movies
```

---

## 🚀 Future Improvements

Possible future improvements include:

* 👤 User-based personalized recommendations
* ⭐ User rating system
* 🔥 Trending movies section
* 🎭 Genre-based filtering
* 🔍 Advanced movie search
* 🌓 Light/Dark theme switch
* 📱 Improved mobile responsiveness
* 🧠 Hybrid recommendation system
* 📊 Recommendation analytics
* ☁️ Cloud deployment
* 🎬 Trailer integration
* ❤️ Favorite/watchlist functionality

---

## 💡 What I Learned

Through this project, I practiced:

* Data preprocessing with Pandas
* Handling JSON-like dataset columns
* Feature engineering
* Natural Language Processing concepts
* TF-IDF vectorization
* Cosine Similarity
* Content-Based Recommendation Systems
* REST API integration
* Streamlit application development
* Environment variable management
* Model testing and evaluation
* Building an end-to-end Machine Learning project

---

## 👨‍💻 Project

**CineMatch AI — Content-Based Movie Recommendation System**

Built using:

```text
Python
Pandas
Scikit-learn
Streamlit
TMDB API
```

---

## 📌 License

This project is intended for educational and portfolio purposes.
