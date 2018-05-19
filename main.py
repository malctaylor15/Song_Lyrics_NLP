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
#nltk.download("stopwords")
#nltk.download("wordnet")
#nltk.download("punkt")

# Word embeddings
# https://nlp.stanford.edu/projects/glove/


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

###############################
#### Class functionalities ####
###############################

#####################
# Song Class Object #
#####################

"""testSong = song('Free Bird', 'Lynyrd Skynyrd') #instantiate a song class object
testSong.getSentiment() # Defines a song class attribute 'polarity'
testSong.showWordCloud()
testSong.getWordCounts()[testSong.getWordCounts() > 3]
print("Test Song Polarity: %s" % testSong.polarity) # Prints same result as getSentiment() calculates"""

#########################
# Playlist class object #
#########################

### Create dataframe of playlists for the user ###

#playlists = sp.category_playlists('hiphop') # For using the genre playlists from spotify
playlists = sp.user_playlists(username) # Returns list of playlists & metadata for the provided user
# Now has list with name and id
playlist_name_id = [(key['name'],  key['owner']['id'], key['tracks']['total'], key['id']) \
                    for key in playlists['items']] # Extract the metadata for each song of the playlist
playlist_name_id
playlist_info = pd.DataFrame(playlist_name_id, columns = ["Name", "Owner", "Number_of_tracks", "Tracklist_id"]) # Set the column names for the playlist metadata
playlist_info = playlist_info.set_index('Name')
playlist_info.columns
keyword = "Feb"
[x for x in playlist_info.index if keyword in x]
playlist_info
playlist_name = "February 2018"

### END Create dataframe of playlists for the user ###
#[playlist(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner, sp) for ]
testPlaylist = playlist(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner, sp)


### 20180301 ###
# Combine multiple playlist?
# Put into separate file for functionality MT_05182018
"""
playlists = list(playlist_info.index)
playlist_info[0:1].index.name
testCompiled = pd.DataFrame(columns=['Title','Artist', 'numb_words', 'Sentiment'])
end = 0
for cat in playlists:
    if end != 3:
        playlist_name = cat
        testPlaylist = playlist(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner, sp)
        playlist_metadata = [(song.title, song.artist, len(song.lyrics.split()), song.getSentiment()) for song in testPlaylist.listOfSongs ]
        playlist_metadata_df = pd.DataFrame(playlist_metadata, columns = ["Title", "Artist", "numb_words" ,"Sentiment"])
        playlist_metadata_df.sort_values("Sentiment", ascending = False)
        playlist_clean = playlist_metadata_df[playlist_metadata_df.Sentiment != 0]
        testCompiled = testCompiled.append(playlist_clean, ignore_index='true')
        end += 1
    else:
        continue
testCompiled
good_songs = testCompiled
"""

### Playlist analysis ###
playlist_metadata = [(song.title, song.artist, len(song.lyrics.split()), song.getSentiment()) for song in testPlaylist.listOfSongs ]
# Reformat the playlist metadata as a list of items to be turned to a dataframe in the next lineplaylist_metadata
playlist_metadata_df = pd.DataFrame(playlist_metadata, columns = ["Title", "Artist", "numb_words" ,"Sentiment"]) # Creating dataframe from running the song class on each song of the playlist given
playlist_metadata_df.sort_values("Sentiment", ascending = False)
good_songs = playlist_metadata_df[playlist_metadata_df.Sentiment != 0] # Filters out songs w/o sentiment
good_songs

# Number songs dropped
len(playlist_metadata) - len(good_songs)
# Number of songs before
len(playlist_metadata)
# Number of songs after
len(good_songs)
# Percentage drop
(1 - len(good_songs)/len(playlist_metadata))*100


good_songs.numb_words.describe()
good_songs.numb_words.plot(kind = "hist")

good_songs.Sentiment.mean()
good_songs.Sentiment.plot(kind = "hist")

###Gather song count by artist###
artist_gb = good_songs.groupby("Artist")
artist_count_all = artist_gb.Title.count() # Not what I wanted but g
artist_count_all

### Gather the average sentiment for the songs of an artist with mroe than 1 song###
artist_count2 = artist_gb.agg({"Title": "count", "Sentiment":"mean"})[artist_gb.count().Title > 1].sort_values("Sentiment", ascending = False)
artist_count2.sort_values(by="Title",ascending=False)

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

### END PLaylist analysis ###


################################
###### Embeddings Analysis #####
################################


######## 05172018

type(testPlaylist)
dir(testPlaylist)
# Get word frequency of top 200 words
testPlaylist.wordFrequency.shape
word_freq_count = testPlaylist.wordFrequency.sum(axis=0)
word_freq_count = word_freq_count.sort_values(ascending=False)
top_words = word_freq_count.index.tolist()
word_freq_count.head()



!pwd
glove_filepath = "/home/malcolm/Downloads/glove.6B.50d.txt"
os.path.isfile(glove_filepath)


cutoff = None # 400000 # max

# Read in the embeddings from the top words list
with open(glove_filepath, 'r+', encoding='utf-8') as fp:
    i = 0
    embed_dict = {}
    for line in fp:
        split_line = line.split()
        if split_line[0] in top_words:
            embed_dict[split_line[0]] = split_line[0:]
        i +=1
        if i % 1000 ==0 :
            print("Looked through ", i, " words")
        if i == cutoff: break
        if len(embed_dict) == len(top_words): break

# Validate embeddings
len(embed_dict)
set(list(embed_dict)).symmetric_difference(top_words)
#list(embed_dict.keys())

# Turn embeddings into dictionary
embed_pd = pd.DataFrame(embed_dict)
embed_pd = embed_pd.T
embed_pd.set_index(embed_pd.iloc[:,0], inplace = True)
embed_pd.drop([0], axis = 1, inplace = True)
embed_pd2 = embed_pd.apply(pd.to_numeric)

embed_pd2.shape
embed_pd2.head(10)

# Find a word using .loc
#embed_pd.loc["much"]


from scipy.spatial.distance import cosine

# Of the top words in the songs, which are closest according to wikipedia 
len(embed_pd2.index) # number of apply loops n x n computations
cosine_dict = {}
for word in embed_pd2.index:
    embed_check = embed_pd2.loc[word]
    temp_single_cosine_list = embed_pd2.apply(lambda x: 1 - cosine(x, embed_check), axis = 1)
    cosine_dict[word] = temp_single_cosine_list.sort_values(ascending = False)


list(cosine_dict.keys())
check_word = "bang"
check_word in embed_pd2.index

cosine_dict[check_word][:5]
