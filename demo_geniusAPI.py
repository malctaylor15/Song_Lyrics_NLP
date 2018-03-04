# Re look into genius API

import requests #web commands module
import re #regular expressions module
from pprint import pprint as pp #pretty printing module
from bs4 import BeautifulSoup #web parser module
import nltk # Natural language processing
from nltk.tokenize import RegexpTokenizer # Regex handler
from nltk.corpus import stopwords # Commonly used words
from nltk.stem.wordnet import WordNetLemmatizer # Convert words into root form
from nltk.stem.porter import PorterStemmer # Strip suffixes from words

song_title = "Candy Cane Lane"
artist_name = "Sia"

base_url = 'https://api.genius.com'
#song_title = "Lake Song"
params = {'q': song_title}
search_url = base_url + '/search'


headers = {'Authorization':'Bearer 8shOdDguRJG7nghujt_1_0HI7Y552WYNWOTbG5a-JAXax6SUVv1Ab4xR55eTwukL'}

#artist_name = "The Decemberists"
resp = requests.get(search_url, params=params, headers=headers)
resp = resp.json()

def lyrics_from_song_api_path(song_api_path, headers):
    """
    This function extracts the lyrics from genius.com using Beautiful Soup
    """
    #print("Running lyrics_from_song_api_path()...") # For Testing
    base_url = 'https://api.genius.com'
    song_url = base_url + song_api_path
    # Query genius for lyrics
    resp  = requests.get(song_url, headers=headers)
    json = resp.json()
    # Find lyrics url, query url
    path = json['response']['song']['path']
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    # Use Beautiful soup to get lyrics text
    html = BeautifulSoup(page.text, 'html.parser')
    [h.extract() for h in html('script')]
    lyrics = html.find("div", class_='lyrics').get_text()
    return lyrics


def text_cleaner(text):
    """
    This function removes various elements from a text.
    It will remove text inside brackets, commas and changes new lines to spaces
    """
    print("Running text_cleaner()...") # For Testing
    lem = WordNetLemmatizer() # Create a lemmatization object
    text = text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    filtered_words = [lem.lemmatize(w) for w in tokens if not w in stopwords.words('english')]
    return " ".join(filtered_words)


for hit in resp['response']['hits']:
    if hit["result"]["primary_artist"]["name"] == artist_name:
        song_info = hit
        break
if song_info:
    song_api_path = song_info['result']['api_path']
    formatted_lyrics = lyrics_from_song_api_path(song_api_path, headers)
    cleaned_lyrics = text_cleaner(formatted_lyrics)
    print("Cleaned lyrics")
else:
    print(song_title,"by", artist_name, "not found in Genius.")
