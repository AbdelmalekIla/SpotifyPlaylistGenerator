from bs4 import BeautifulSoup
import requests
from pprint import pprint
import lxml
spotify_client_id = "be814b434e0740d8be2bd4ca9c6aa802"
spotify_secret_client = "769918b5e39a48768fdc043fa14c1621"

date = input('which year you want? please type the date in this format YYYY-MM-DD\n')
url = "https://www.billboard.com/charts/hot-100"
data = requests.get(f"{url}/{date}")
html_data = data.text

soup = BeautifulSoup(html_data, 'html.parser')

song_title = soup.select("ul li ul li h3")

top_100_song_list = [i.getText().strip() for i in song_title]
print(top_100_song_list)


