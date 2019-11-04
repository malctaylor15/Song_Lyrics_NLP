# coding: utf-8

import requests #web commands module
#import re #regular expressions module

import nltk # Natural language processing
from nltk.tokenize import RegexpTokenizer # Regex handler
from nltk.corpus import stopwords # Commonly used words
from nltk.stem.wordnet import WordNetLemmatizer # Convert words into root form
#from nltk.stem.porter import PorterStemmer # Strip suffixes from words

#from pprint import pprint as pp #pretty printing module
from bs4 import BeautifulSoup #web parser module


def get_lyrics_from_genius_page(path):
    """
    This function extracts the lyrics from genius.com using Beautiful Soup
    """

    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    if (page.status_code < 200) or (page.status_code >= 300):
        print("Debug: Could not find page for " + page_url)
        return None
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
    #print("Running text_cleaner()...") # For Testing
    lem = WordNetLemmatizer() # Create a lemmatization object
    text = text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    filtered_words = [lem.lemmatize(w) for w in tokens if not w in stopwords.words('english')]
    return " ".join(filtered_words)

def get_song_lyrics(artist_name, song_title, headers):
    """
    This function checks the genius api to see if an artist and song name combination is in the genius api function family.
    This function will return the lyrics if they are available on genius.com
    It will also run the text cleaner on the lyrics to remove unwanted characters

    Inputs:
        artist_name = requested artist name (string)
        song_title = Requested song name (string)
        headers = Genius header authorization keys (dictionary)
    Output:
        cleaned_lyrics = lyrics after being cleaned by text cleaner function
        ' ' = if the lyrics are not found
    """
    #print("Running get_song_lyrics()...") # For testing
    base_url = 'https://api.genius.com'
    #song_title = "Lake Song" # For testing
    params = {'q': song_title}
    search_url = base_url + '/search'

    #artist_name = "The Decemberists"
    resp = requests.get(search_url, params=params, headers=headers)
    resp = resp.json()
    #pp(resp)
    lyrics_path = None

    #pp(resp['response']['hits'])
    for hit in resp['response']['hits']:
        #print(hit["result"]) # for testing
        if hit["result"]["primary_artist"]["name"].lower() == artist_name.lower():
            lyrics_path = hit['path']
            break

    if lyrics_path == None:
        # print('No hit found in genius api.. trying custom lookup link')
        lyrics_path = create_fake_link(artist_name, song_title)

    genius_lyrics = get_lyrics_from_genius_page(lyrics_path)
    if genius_lyrics != None:
        return(genius_lyrics)
    else:
        print(f"\t{artist_name}'s {song_title} not in Genius.")
        return(' ')

#test_lyrics = get_song_lyrics(artist_name="Kendrick Lamar", song_title="HUMBLE.", headers=headers)
#print(test_lyrics

def quick_clean_str(string):
    string = string.replace('.', '')
    string = string.replace(' ', '-')
    return(string)

def create_fake_link(artist, title):
    artist_clean = quick_clean_str(artist)
    artist_clean = artist_clean.capitalize()
    title_clean = quick_clean_str(title).lower()
    link = '/'+artist_clean+'-'+title_clean+'-lyrics'
    return(link)
