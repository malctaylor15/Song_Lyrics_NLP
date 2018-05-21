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

from scipy.spatial.distance import cosine


# Get user playlist information from spotify
#username = 'malchemist02'  #TODO: Make user input
username = "1282829978"
scope = 'user-library-read playlist-read-private user-top-read' #the permissions to give our application
token = util.prompt_for_user_token(username,scope)
sp = spotipy.Spotify(auth=token)

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
keyword = "Sing"
[x for x in playlist_info.index if keyword in x]
playlist_info
playlist_name = "Discover Weekly Archive"


#testPlaylist = playlist(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner, sp)
testPlaylist = playlist("37i9dQZF1DWWMOmoXKqHTD", "spotify", sp)



######## 05172018

type(testPlaylist)
dir(testPlaylist)
# Get word frequency of top 200 words
# testPlaylist.wordFrequency.shape
# word_freq = testPlaylist.wordFrequency
word_freq = testPlaylist.getWordCounts(300)



word_freq_count = word_freq.sum(axis=0)
word_freq_count = word_freq_count.sort_values(ascending=False)

song_freq_count = word_freq.sum(axis=1)
song_freq_count = song_freq_count.sort_values(ascending=False)

# Drop songs with no words
word_freq = word_freq.drop([x[0] for x in song_freq_count.iteritems() if x[1] == 0],axis = 0)
song_freq_count2 = song_freq_count[song_freq_count != 0]
len(song_freq_count2)
song_freq_count.shape
word_freq.shape
# word_freq

# song_freq_count.head()
# word_freq_count.head()
top_words = word_freq_count.index.tolist()





!pwd
# glove_filepath = "/home/owner/Downloads/glove.6B.50d.txt"
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
        if i % 4000 ==0 :
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


# from scipy.spatial.distance import cosine

# Of the top words in the playlist, which are closest according to wikipedia
len(embed_pd2.index) # number of apply loops n x n computations
cosine_dict = {}
for word in embed_pd2.index:
    embed_check = embed_pd2.loc[word]
    temp_single_cosine_list = embed_pd2.apply(lambda x: 1 - cosine(x, embed_check), axis = 1)
    cosine_dict[word] = temp_single_cosine_list.sort_values(ascending = False)


list(cosine_dict.keys())
check_word = "girl"
check_word in embed_pd2.index
cosine_dict[check_word][:10]

## 05192017

embed_pd2.shape
embed_pd2.head()
word_freq.shape
word_match_freq = word_freq.drop([col for col in word_freq.columns \
if col not in list(embed_dict.keys())],axis = 1)
word_freq.head()
song_embeds = word_match_freq.dot(embed_pd2)
song_embeds.head()
song_embeds

song_freq_count.head()
song_freq_count.shape
song_embeds.shape

# Normalize embededdings -- some songs have more words than others
norm_song_embeds = song_embeds.divide(song_freq_count2, axis = 0)

norm_song_embeds.head()

song_cosine_dict = {}
for song in norm_song_embeds.index:
    embed_check = norm_song_embeds.loc[song]
    temp_single_cosine_list = norm_song_embeds.apply(lambda x: 1 - cosine(x, embed_check), axis = 1)
    song_cosine_dict[song] = temp_single_cosine_list.sort_values(ascending = False)

# Songs that are similar to each other
[(song, x[:5]) for song, x in song_cosine_dict.items()]
# Song that are dissimilar to each other
[(song, x[-5:]) for song, x in song_cosine_dict.items()]


######## Compare embedding regression to using only the words

dir(testPlaylist)


### Get sentiment as response variable ###
playlist_metadata = [(song.title, song.artist, len(song.lyrics.split()), song.getSentiment()) for song in testPlaylist.listOfSongs ]
playlist_metadata_df = pd.DataFrame(playlist_metadata, columns = ["Title", "Artist", "numb_words" ,"Sentiment"]) # Creating dataframe from running the song class on each song of the playlist given
playlist_metadata_df.sort_values("Sentiment", ascending = False)
playlist_metadata_df = playlist_metadata_df[playlist_metadata_df.numb_words > 0]
playlist_metadata_df.set_index("Title", inplace = True)
playlist_metadata_df.shape
playlist_metadata_df.sort_values("Sentiment", ascending = False).head()



####### Join embedings df1
embeding_model_df1 = playlist_metadata_df.join(norm_song_embeds)
embeding_model_df1.drop(["Artist"], axis = 1, inplace = True)
embeding_model_df1.shape

### Word freq df
freq_model_df1 = playlist_metadata_df.join(word_freq)
freq_model_df1.drop(["Artist"], axis = 1, inplace = True)
freq_model_df1.shape # Includes sentiment and # of words
freq_model_df1.head()


from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

X_em = embeding_model_df1.drop(["Sentiment"], axis = 1)
Y_em = embeding_model_df1["Sentiment"]

X_train, X_test, y_train, y_test = train_test_split(X_em, Y_em)

fit1 = LinearRegression().fit(X_train, y_train)
fit1.score(X_test, y_test)
dir(LinearRegression)



X_nw = freq_model_df1.drop(["Sentiment"], axis = 1)
Y_nw = freq_model_df1["Sentiment"]
X_train, X_test, y_train, y_test = train_test_split(X_nw, Y_nw)

fit2 = LinearRegression().fit(X_train, y_train)
fit2.score(X_test, y_test)
dir(LinearRegression)


########### Use a cosine similarity as dep var... compare performance
song_cosine_dict.keys()
dep_var2 = song_cosine_dict["All of Me"]
dep_var2.join(...)
