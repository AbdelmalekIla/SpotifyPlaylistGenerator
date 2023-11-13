from bs4 import BeautifulSoup
import requests
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


spotify_client_id = os.environ["SPOTIFY_CLIENT_ID"]
spotify_secret_client = os.environ['SPOTIFY_SECRET_CLIENT']


date = input('which year you want? please type the date in this format YYYY-MM-DD\n')
year = date.split('-')[0]
scope = 'playlist-modify-private'
url = "https://www.billboard.com/charts/hot-100"
data = requests.get(f"{url}/{date}")
html_data = data.text

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                                    client_secret=spotify_secret_client,
                                                    redirect_uri='http://example.com',
                                                    scope=scope,
                                                    cache_path='token.txt'
                                                    ))
sp_data = spotify.current_user()
user_id = sp_data['id']

soup = BeautifulSoup(html_data, 'html.parser')

song_title = soup.select("ul li ul li h3")

top_100_song_list = [i.getText().strip() for i in song_title]

uri_list = [spotify.search(q=f"track:{i} year:{year}", type='track')['tracks']['items'][0]['uri'] for i in
            top_100_song_list]
new_playlist = spotify.user_playlist_create(user=user_id, name=f'{date} Billboard 100', public=False, description='pass XD')
playlist_data = new_playlist['id']

spotify.playlist_add_items(playlist_id=playlist_data, items=uri_list)