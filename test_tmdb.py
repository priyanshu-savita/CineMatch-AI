import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TMDB_ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "accept": "application/json"
}

movie_ids = {
    1865: "Pirates of the Caribbean: On Stranger Tides",
    87827: "Life of Pi",
    72197: "The Pirates! In an Adventure with Scientists!"
}

for movie_id, title in movie_ids.items():

    print("\n" + "=" * 60)
    print("Testing:", title)
    print("Movie ID:", movie_id)

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        print("Status:", response.status_code)

        if response.status_code == 200:

            data = response.json()

            print("TMDB Title:", data.get("title"))
            print("Poster Path:", data.get("poster_path"))
            print("Rating:", data.get("vote_average"))
            print("Release Date:", data.get("release_date"))

        else:
            print("Response:")
            print(response.text)

    except requests.exceptions.RequestException as error:
        print("Connection error:", error)