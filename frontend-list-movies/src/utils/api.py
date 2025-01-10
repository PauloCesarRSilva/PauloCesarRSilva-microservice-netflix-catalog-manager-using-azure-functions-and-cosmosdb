def fetch_videos(api_url):
    import requests

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()  # Assuming the API returns a JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching videos: {e}")
        return []  # Return an empty list on error