from bs4 import BeautifulSoup
import requests
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth

spotify_client_id = 'be814b434e0740d8be2bd4ca9c6aa802'
spotify_secret_client = '769918b5e39a48768fdc043fa14c1621'
spotify_get_token_url = 'https://accounts.spotify.com/api/token'
scope = 'playlist-modify-private'
date = input('which year you want? please type the date in this format YYYY-MM-DD\n')
year = date.split('-')[0]
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

print(uri_list)
