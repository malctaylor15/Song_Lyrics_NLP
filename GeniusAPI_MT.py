
# coding: utf-8

# In[1]:

import requests
from pprint import pprint as pp
from bs4 import BeautifulSoup
import re


# In[2]:

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


# In[4]:

def text_cleaner(text): 
    """ 
    This function removes various elements from a text. 
    It will remove text inside brackets, commas and changes new lines to spaces 
    """
    
    numb_open_bracket = text.count('[')
    numb_closed_bracket = text.count(']')
    if numb_open_bracket != numb_closed_bracket:
        print("Unequal number of open and closed brackets... \n May have deleted content")
    
    temp_text = re.sub(r'\[.*?\]', '', text)
    temp_text = re.sub(r',', '', temp_text)
    temp_text = temp_text.replace('\n', ' ')

    print("Length of text before cleaning: ", len(text))
    print("Length of text after cleaning: ", len(temp_text))
    return(temp_text)


# In[3]:

def get_song_lyrics(artist_name, song_title, headers):
    """
    This function checks the genius api to see if an artist and song name combination is in the genius api function family. 
    If the song's lyrics are available on genius, this function will return the lyrics 
    """
    
    base_url = 'https://api.genius.com'
    #song_title = "Lake Song"
    params = {'q': song_title}
    search_url = base_url + '/search'
    
    #artist_name = "The Decemberists"
    resp = requests.get(search_url, params=params, headers=headers)
    resp = resp.json()#['response']['song']
    #pp(resp)
    song_info = None

    #pp(resp['response']['hits'])
    for hit in resp['response']['hits']:
        if hit["result"]["primary_artist"]["name"] == artist_name:
            song_info = hit
            break
    if song_info:
        song_api_path = song_info['result']['api_path']
        formattedLyrics = lyrics_from_song_api_path(song_api_path, headers)
        cleaned_lyrics = text_cleaner(formattedLyrics)
        return(cleaned_lyrics)
    else:
        print("Did not find Artist: ", artist_name, " Song: ", song_title, " combination.")
        return() 


# In[5]:

headers = {'Authorization':'Bearer 8shOdDguRJG7nghujt_1_0HI7Y552WYNWOTbG5a-JAXax6SUVv1Ab4xR55eTwukL'}


# In[6]:

#lyrics1 = get_song_lyrics(artist_name="Kendrick Lamar", song_title="HUMBLE", headers=headers)
#clean_lyrics = text_cleaner(lyrics1)


# In[ ]:




# In[ ]:




# In[ ]:



