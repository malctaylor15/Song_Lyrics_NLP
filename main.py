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

from song import song
from playlist import playlist

# Get user playlist information from spotify
username = '1282829978'  #TODO: Make user input
scope = 'user-library-read playlist-read-private user-top-read' #the permissions to give our application
token = util.prompt_for_user_token(username,scope)
sp = spotipy.Spotify(auth=token)
playlists = sp.user_playlists(username)

# Look at user playlist name, number of tracks, and spotify tracklist id
playlists_info = get_user_playlists_2(username, playlists)
print(playlists_info)
type(playlists_info)


spotify_tracklist_id = playlists_info.Tracklist_id.loc[3]
print(spotify_tracklist_id)
tracklist = get_tracklist_class(spotify_tracklist_id, username, sp) # Look at songs in playlist

#############################################
#### Begin Testing class functionalities ####
#############################################

### Song Object Functionality ###
testSong = song('Free Bird', 'Lynyrd Skynyrd') #instantiate a song class object
testSong.getSentiment()
testSong.showWordCloud()
print(testSong.polarity) # Same as getSentiment()
# running getSentiment will define song class attribute polarity


############################################################

### Testing playlist class object funcTIonality
playlists = sp.category_playlists('hiphop')

# NOTE... can delete later
[key for key in playlists.keys()]
[key for key in playlists['playlists'].keys()]
[key for key in playlists['playlists']['items']]
[key for key in playlists['playlists']['items'][0].keys()]

# Now has list with name and id
playlist_name_id = [(key['name'],  key['owner']['id'],key['tracks']['total'] , key['id']) \
                    for key in playlists['playlists']['items']]

playlist_info = pd.DataFrame(playlist_name_id, columns = ["Name", "Owner", "Number_of_tracks", "Tracklist_id"])
playlist_info

# NOTE... can delete later
playlist_info[playlist_info.Name == "Gold School"].Tracklist_id

# Way two
playlist_info.index = playlist_info.Name
playlist_info.loc["Gold School"].Tracklist_id
playlist_info.loc["Gold School"].Owner

testPlaylist = playlist('37i9dQZF1DX0XUsuxWHRQd', 'spotify', sp)

playlist_sent_l = [(song.title, song.artist, len(song.lyrics.split()), song.getSentiment()) for song in testPlaylist.listOfSongs ]
song_name_sent = pd.DataFrame(playlist_sent_l, columns = ["Title", "Artist", "Numb_words_in_song" ,"Sentiment"])
song_name_sent.sort_values("Sentiment", ascending = False)
# Songs without sentiment
good_songs = song_name_sent[song_name_sent.Sentiment != 0]

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


artist_gb = good_songs.groupby("Artist")
# NOTE... can delete later
artist_count_all = artist_gb.Title.count() # Not what I wanted but good example
# Applies count to all columns .. only want to count titles
# Not sure how to do but...

artist_count2 = artist_gb.agg({"Title": "count", "Sentiment":"mean"})[artist_gb.count().Title > 1].sort_values("Sentiment", ascending = False)

artist_count2


###20180206 testing ###
from nltk.corpus import words
word_list = words.words()
# prints 236736
type(word_list)
print(len(word_list))



#20180206
###################################################
song_lyrics = [song.lyrics for song in testPlaylist.listOfSongs]
type(song_lyrics[0])
songLyricsNonEmpty = [lyrics for lyrics in song_lyrics if lyrics != ' ']

lyrics1 = ''
for lyrics in songLyricsNonEmpty:
    lyrics1 = lyrics1 + " " +  lyrics
lyrics1
len(lyrics1)
len(nltk.word_tokenize(lyrics1))
demoLyrics = list(set(nltk.word_tokenize(lyrics1)))
demoLyrics.sort()

slang = [word for word in demoLyrics if word not in word_list]
len(slang)
slang
[word for word in word_list if word == "attended"]

import enchant
d = enchant.Dict("en_US")
d.check("Hello")
d.check("Helo")
d.suggest("Helo")




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
