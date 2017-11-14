# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 20:30:13 2017

@author: drose
"""
import requests
from pprint import pprint as pp
from bs4 import BeautifulSoup

def lyrics_from_song_api_path(song_api_path):

    song_url = base_url + song_api_path
    resp  = requests.get(song_url, headers=headers)
    json = resp.json()
    path = json['response']['song']['path']
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, 'html.parser')
    [h.extract() for h in html('script')]
    lyrics = html.find("div", class_='lyrics').get_text()
    return lyrics

def get_api_path():
    base_url = 'https://api.genius.com'
    headers = {'Authorization':'Bearer vXtl426Pm3yYJdhnbnMOI6kP4VH23TtHUWd463eSXWeGeP-YB7PrvwQOt5k6tm-c'}
    song_title = "HUMBLE."
    params = {'q': song_title}
    search_url = base_url + '/search'
    
    artist_name = "Kendrick Lamar"
    resp = requests.get(search_url, params=params, headers=headers)
    resp = resp.json()
    song_info = None

    #pp(resp['response']['hits'])
    for hit in resp['response']['hits']:
        if hit["result"]["primary_artist"]["name"] == artist_name:
            song_info = hit
            break
    if song_info:
        song_api_path = song_info['result']['api_path']
        
        formattedLyrics = lyrics_from_song_api_path(song_api_path)
        print(formattedLyrics)
        unformattedLyrics = formattedLyrics.replace('\n', ' ')
        print(unformattedLyrics)
        #now we have the song info and can do what we want
    #print(song_info)
    
get_api_path()