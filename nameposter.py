import requests

# Define the OMDb API key as a global constant
OMDB_API_KEY = "d6398547"  # Replace with your OMDb API key

def get_movie_details_by_id(imdb_id):
    """
    Fetch the movie name and poster URL using the IMDb ID.

    Args:
    - imdb_id (str): The IMDb ID of the movie.

    Returns:
    - tuple: (movie_name, poster_url) or an error message and None if unsuccessful.
    """
    # Construct the API URL using the IMDb ID
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
    
    try:
        # Send a GET request to the OMDb API
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Check if the movie was found
        if data.get("Response") == "True":
            movie_name = data.get("Title", "N/A")
            poster_url = data.get("Poster", "Poster not available.")
            return movie_name, poster_url
        else:
            return "Movie not found.", None
    except requests.exceptions.RequestException as e:
        return f"Failed to fetch movie details: {str(e)}", None

# Usage example (for testing purposes)
if __name__ == "__main__":
    imdb_id = input("Enter the IMDb ID: ")  # Get IMDb ID from the user
    
    movie_name, poster_url = get_movie_details_by_id(imdb_id)
    print(f"Movie Name: {movie_name}")
    print(f"Movie Poster URL: {poster_url}")
