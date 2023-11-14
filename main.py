from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Retrieve Spotify credentials from environment variables
spotify_client_id = os.environ["SPOTIFY_CLIENT_ID"]
spotify_secret_client = os.environ['SPOTIFY_SECRET_CLIENT']

# Get the desired year from user input
date = input('which year you want? please type the date in this format YYYY-MM-DD\n')

# Set up Spotify authentication scope and Billboard Hot 100 URL
scope = 'playlist-modify-private'
url = "https://www.billboard.com/charts/hot-100"

# Scrape Billboard Hot 100 data for the specified date
data = requests.get(f"{url}/{date}")
html_data = data.text

# Authenticate with Spotify using Spotipy
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                                    client_secret=spotify_secret_client,
                                                    redirect_uri='http://example.com',
                                                    scope=scope,
                                                    cache_path='token.txt'
                                                    ))
sp_data = spotify.current_user()
user_id = sp_data['id']

# Parse HTML data using BeautifulSoup
soup = BeautifulSoup(html_data, 'html.parser')

# Extract song titles from the Billboard Hot 100
song_title = soup.select("ul li ul li h3")
top_100_song_list = [i.getText().strip() for i in song_title]

# Search for Spotify URIs for each song
uri_list = [spotify.search(q=i, type='track')['tracks']['items'][0]['uri'] for i in
            top_100_song_list]

# Create a new private playlist on Spotify
new_playlist = spotify.user_playlist_create(user=user_id, name=f'{date} Billboard 100', public=False,
                                            description='pass XD')
playlist_data = new_playlist['id']

# Add the Spotify URIs to the newly created playlist
spotify.playlist_add_items(playlist_id=playlist_data, items=uri_list)
