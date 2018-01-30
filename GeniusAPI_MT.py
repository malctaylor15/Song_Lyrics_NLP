# coding: utf-8
#test android change
import requests #web commands module
import re #regular expressions module

import nltk # Natural language processing
from nltk.tokenize import RegexpTokenizer # Regex handler
from nltk.corpus import stopwords # Commonly used words

from pprint import pprint as pp #pretty printing module
from bs4 import BeautifulSoup #web parser module

headers = {'Authorization':'Bearer 8shOdDguRJG7nghujt_1_0HI7Y552WYNWOTbG5a-JAXax6SUVv1Ab4xR55eTwukL'}

def lyrics_from_song_api_path(song_api_path, headers):
    """
    This function extracts the lyrics from genius.com using Beautiful Soup
    """

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
    text = text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    filtered_words = [w for w in tokens if not w in stopwords.words('english')]
    return " ".join(filtered_words)
"""    numb_open_bracket = text.count('[')
    numb_closed_bracket = text.count(']')
    if numb_open_bracket != numb_closed_bracket:
        print("Unequal # of open & closed brackets... \n May have deleted content")

    temp_text = re.sub(r'\[.*?\]', '', text)
    temp_text = re.sub(r',', '', temp_text) # Replace commas with nothing
    temp_text = temp_text.replace('(', '') # Delete '('
    temp_text = temp_text.replace(')', '') # Delete ')'
    temp_text = temp_text.replace('\n', ' ') # Replace new line with space
    temp_text = temp_text.replace('?', '') # Delete '?'
    temp_text = temp_text.replace('!', '') # Delete '!'

    #print("Pre-cleaning chars: ", len(text))
    #print("Post-cleaning chars: ", len(temp_text))
    print("Removed", len(text) - len(temp_text), "characters during cleaning.")
    return(temp_text)"""

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

    base_url = 'https://api.genius.com'
    #song_title = "Lake Song"
    params = {'q': song_title}
    search_url = base_url + '/search'

    #artist_name = "The Decemberists"
    resp = requests.get(search_url, params=params, headers=headers)
    resp = resp.json()
    #pp(resp)
    song_info = None

    #pp(resp['response']['hits'])
    for hit in resp['response']['hits']:
        if hit["result"]["primary_artist"]["name"] == artist_name:
            song_info = hit
            break
    if song_info:
        song_api_path = song_info['result']['api_path']
        formatted_lyrics = lyrics_from_song_api_path(song_api_path, headers)
        cleaned_lyrics = text_cleaner(formatted_lyrics)
        return(cleaned_lyrics)
    else:
        print(song_title,"by", artist_name, "not found in Genius.")
        return(' ')

#test_lyrics = get_song_lyrics(artist_name="Kendrick Lamar", song_title="HUMBLE.", headers=headers)
#print(test_lyrics)
