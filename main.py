# System utilities
import os
from os import environ
import subprocess
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

# Spotify API
import spotipy
import spotipy.util as util

from importlib import reload
import GeniusAPI_MT
reload(GeniusAPI_MT)
from GeniusAPI_MT import *

import Spotify_Pulls
reload(Spotify_Pulls)
from Spotify_Pulls import *

import song
reload(song)
from song import song

import playlist
reload(playlist)
from playlist import playlist


# Get user playlist information from spotify
username = 'malchemist02'  #TODO: Make user input
scope = 'user-library-read playlist-read-private user-top-read' #the permissions to give our application
token = util.prompt_for_user_token(username,scope)
sp = spotipy.Spotify(auth=token)

#############################################
#### Begin Testing class functionalities ####
#############################################

### Song Object Functionality ###
testSong = song('Free Bird', 'Lynyrd Skynyrd') #instantiate a song class object
testSong.getSentiment()
testSong.showWordCloud()
testSong.getWordCounts()[testSong.getWordCounts() > 3]
print(testSong.polarity) # Same as getSentiment()
# running getSentiment will define song class attribute polarity

############################################################

### Testing playlist class object functionality

#playlists = sp.category_playlists('hiphop')
playlists = sp.user_playlists(username)

# Now has list with name and id
playlist_name_id = [(key['name'],  key['owner']['id'], key['tracks']['total'], key['id']) \
                    for key in playlists['items']] # Extract the metadata for each song of the playlist
playlist_name_id
playlist_info = pd.DataFrame(playlist_name_id, columns = ["Name", "Owner", "Number_of_tracks", "Tracklist_id"]) # Set the column names for the playlist metadata
playlist_info.columns

playlist_name = "May 2015"
playlist_info = playlist_info.set_index('Name')

testPlaylist = playlist(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner, sp)

### Start playlist analysis ###
playlist_sent_l = [(song.title, song.artist, len(song.lyrics.split()), song.getSentiment()) for song in testPlaylist.listOfSongs ]
song_name_sent = pd.DataFrame(playlist_sent_l, columns = ["Title", "Artist", "Numb_words_in_song" ,"Sentiment"]) # Creating dataframe from running the song class on each song of the playlist given
song_name_sent.sort_values("Sentiment", ascending = False)

good_songs = song_name_sent[song_name_sent.Sentiment != 0] # Filters out songs w/o sentiment

# Number songs dropped
len(playlist_sent_l) - len(good_songs)
# Number of songs before
len(playlist_sent_l)
# Number of songs after
len(good_songs)
# Percentage drop
(1 - len(good_songs)/len(playlist_sent_l))*100


good_songs.Numb_words_in_song.describe()
good_songs.Numb_words_in_song.plot(kind = "hist")

good_songs.Sentiment.mean()
good_songs.Sentiment.plot(kind = "hist")

###Gather song count by artist###
artist_gb = good_songs.groupby("Artist")
artist_count_all = artist_gb.Title.count() # Not what I wanted but g
artist_count_all

### Gather the average sentiment for the songs of an artist with mroe than 1 song###
artist_count2 = artist_gb.agg({"Title": "count", "Sentiment":"mean"})[artist_gb.count().Title > 1].sort_values("Sentiment", ascending = False)
artist_count2

### Song analysis ###
song_demo = testPlaylist.listOfSongs[1]
song_demo.getWordCounts()
song_demo.title

vect = CountVectorizer()
words = [word for word in song_demo.lyrics.split()]

len([word for word in song_demo.lyrics.split() if word == "tu"])

words[:4]
[song_demo.lyrics]
feats = vect.fit_transform([song_demo.lyrics]).toarray()[0]
song.getWordCounts(song_demo)
pd.Series(feats, index = vect.get_feature_names()).T.sort_values(ascending = False)
feats


###################################################
song_lyrics = [song.lyrics for song in testPlaylist.listOfSongs]
songLyricsNonEmpty = [lyrics for lyrics in song_lyrics if lyrics != ' ']
songLyricsNonEmpty

lyrics1 = ''
for lyrics in songLyricsNonEmpty:
    lyrics1 = lyrics1 + " " +  lyrics # Combine the lyrics of all the songs into one string
lyrics1
len(lyrics1)
len(nltk.word_tokenize(lyrics1))
demoLyrics = list(set(nltk.word_tokenize(lyrics1)))
demoLyrics.sort()
demoLyrics

songLyricsNonEmpty = [lyrics1+lyrics for lyrics in songLyricsNonEmpty]
songLyricsNonEmpty
' '.join(songLyricsNonEmpty)
testPlaylist.getWordCounts().iloc[0]
testPlaylist.getTfidf()
wordFrequency = testPlaylist.getWordCounts()
wordFrequency
#############################################################

### Get the words showing in all the songs of a playlist ### 20180129
songList = testPlaylist.getTfidf()#.drop("F**kin' Problems",axis=0)
songList.T[songList.apply(lambda col: col.all((0)),axis=0)]

#wc1 = WordCloud().generate(wc_corpus)
#wc1.to_image().show()
################################################################################################
