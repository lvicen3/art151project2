import requests
import re
import random

from bs4 import BeautifulSoup
from utils import get_tokens, get_stopwords
from flask import Flask, render_template

app = Flask(__name__)

stopwords = get_stopwords()	
bands = ['Vampire_Weekend', 'Radiohead', 'U2']
N_LINES = 3
random.seed(300)

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

def get_art(words):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://unsplash.com/s/photos/{0}-{1}-{2}'.format(words[0],words[1],words[2])
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content,'html.parser')
    figures = soup.findAll('figure')
    img_links = []
    for figure in figures:
        try:
            img_links.append(figure.find('img').get('src'))
        except:
            ()        
    
    img_links = [img_link for img_link in img_links if re.match(r'(.+)photo(.+)', img_link)]

    return random.choice(img_links)

#set route for user navigation
@app.route('/')

def index():
    return render_template("index.html")

@app.route('/first_band')

def first_band():
    lines = []
    for i in range(N_LINES):
        lines.append(get_random_line(bands[0]))
    
    word_sets = []
    for line in lines:
        temp = []
        for word in get_tokens(line):
            if word in stopwords:
                temp.append(get_tokens(line))
        words.append(temp)

    img_words = [random.choice(word_set) for word_set in word_sets]

    img_url = get_art(img_words)

    return render_template('first_band.html', band_names=bands[0], lines = lines,img_url=img_url)

@app.route('/second_band')

def second_band():
    lines = []
    for i in range(N_LINES):
        lines.append(get_random_line(bands[1]))
    
    return render_template('second_band.html', band_names=bands[1], lines = lines)

@app.route('/third_band')

def third_band():
    lines = []
    for i in range(N_LINES):
        lines.append(get_random_line(bands[2]))
    
    return render_template('third_band.html', band_names=bands[2], lines = lines)