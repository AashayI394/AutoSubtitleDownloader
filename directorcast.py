import requests

# Define the API key as a constant at the module level
TMDB_API_KEY = "f1262dc0c80b1b08fa6d8308b0cc67bd"  # Replace with your TMDB API key

def get_director_and_cast(imdb_id):
    """
    Fetch the director and main cast members for a given IMDb ID using the TMDB API.

    Args:
    - imdb_id (str): IMDb ID of the movie (e.g., "tt1375666").

    Returns:
    - dict: A dictionary with director and cast details.
    """
    base_url = "https://api.themoviedb.org/3"

    try:
        # Step 1: Get TMDB ID from IMDb ID
        find_url = f"{base_url}/find/{imdb_id}"
        find_params = {"api_key": TMDB_API_KEY, "external_source": "imdb_id"}
        find_response = requests.get(find_url, params=find_params)
        find_response.raise_for_status()

        find_data = find_response.json()
        if "movie_results" in find_data and find_data["movie_results"]:
            tmdb_id = find_data["movie_results"][0]["id"]
        else:
            return {"error": "No movie found for the given IMDb ID."}

        # Step 2: Get credits information using TMDB ID
        credits_url = f"{base_url}/movie/{tmdb_id}/credits"
        credits_params = {"api_key": TMDB_API_KEY}
        credits_response = requests.get(credits_url, params=credits_params)
        credits_response.raise_for_status()

        credits_data = credits_response.json()

        # Extract director
        director = None
        for crew_member in credits_data.get("crew", []):
            if crew_member["job"] == "Director":
                director = crew_member["name"]
                break

        # Extract main cast
        main_cast = [cast_member["name"] for cast_member in credits_data.get("cast", [])[:5]]  # Top 5 cast members

        return {
            "director": director,
            "main_cast": main_cast
        }

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    imdb_id = input("Enter IMDb ID (e.g., tt1375666): ")

    result = get_director_and_cast(imdb_id)
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Director: {result['director']}")
        print("Main Cast:")
        for actor in result["main_cast"]:
            print(f"- {actor}")
