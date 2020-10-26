from bs4 import BeautifulSoup
import requests
import re
import random
from flask import Flask, render_template

app = Flask(__name__)

bands = ['Vampire_Weekend', 'Radiohead', 'U2']

# Function to split a document into a list of tokens
# Arguments:
# doc: A string containing input document
# Returns: tokens (list)
# Where, tokens (list) is a list of tokens that the document is split into
def get_tokens(doc):
	tokens = re.split(r"[^A-Za-z0-9-']", doc)
	tokens = list(filter(len, tokens))
	return tokens

def get_random_line(band_name='Vampire_Weekend'):
  # # pull discography table from band's wiki
  try:
    url = 'https://en.wikipedia.org/wiki/{0}_discography'.format(band_name)
    page = requests.get('https://en.wikipedia.org/wiki/{0}_discography'.format(band_name))
    discography_soup = BeautifulSoup(page.content,'html.parser')
  except:
    print('Error opening artist link')
    raise
  
  album_list = discography_soup.find(attrs={'id':'Studio_albums'}).findNext('table', attrs={'class': 'wikitable plainrowheaders'}).find_all('th',attrs={'scope':'row'})

  album_urls = []
  for album in album_list:
      album_urls.append('https://en.wikipedia.org/'+album.find('a')['href'])
  album_url = random.choice(album_urls)

  # pull album page -> get a song
  album_page = requests.get(album_url)
  album_soup = BeautifulSoup(album_page.content,'html.parser')
  songs = album_soup.find('table',attrs={'class':'tracklist'}).find_all(attrs={'style':'vertical-align:top'})
  song = random.choice(songs).get_text()
  song = re.sub(r'\([^)]*\)','',song)
  song = song.lower()
  # song = song.replace('"','').lower().replace(' ','-')
  song = get_tokens(song)
  parsed_song = ''
  for word in song[:-1]:
      parsed_song+=word + '-'
  parsed_song+=song[-1]  

  # build url for genius website
  # parsed_song = ((re.search('"(\w[\s\w]*)"', song).group(1)).lower()).replace(' ','-')
  parsed_band = band_name.lower().capitalize().replace('_','-')
  genius_url = 'https://genius.com/' + parsed_band + '-' + parsed_song + '-lyrics'
  
  # page = requests.get('https://genius.com/Vampire-weekend-hannah-hunt-lyrics')
  page = requests.get(genius_url)
  soup = BeautifulSoup(page.content,'html.parser')
  lyrics = soup.find('p')

  lyrics_str = lyrics.get_text()
  lyrics_str = re.sub(r'\[[^]]*\][\n\r]','',lyrics_str)
  lines = re.split(r'[\n\r]+', lyrics_str)
  
  return random.choice(lines)

#set route for user navigation
@app.route('/')

def index():
    return render_template("index.html")

@app.route('/first_band')

def first_band():
    lines = []
    for i in range(3):
        lines.append(get_random_line(bands[0]))
    
    return render_template('first_band.html', text = '123')

@app.route('/second_band')

def second_band():
    lines = []
    for i in range(3):
        lines.append(get_random_line(bands[1]))
    
    return render_template('second_band.html', text = '123')

@app.route('/third_band')

def third_band():
    lines = []
    for i in range(3):
        lines.append(get_random_line(bands[2]))
    
    return render_template('third_band.html', text = '123')