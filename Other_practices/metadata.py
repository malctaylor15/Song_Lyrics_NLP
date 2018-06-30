# System utilities

%matplotlib inline

from importlib import reload

import numpy as np
# Spotify API
import spotipy
import spotipy.util as util

import genius_api

reload(genius_api)

import playlist_class

reload(playlist_class)
from playlist_class import *

import song_class

reload(song_class)

import playlist_class
reload(playlist_class)
from playlist_class import playlist


# Get user playlist information from spotify
username = 'malchemist02'  #TODO: Make user input
scope = 'user-library-read playlist-read-private user-top-read' #the permissions to give our application
token = util.prompt_for_user_token(username,scope)
sp = spotipy.Spotify(auth=token)

playlists = sp.user_playlists(username) # Returns list of playlists & metadata for the provided user
playlists

playlist_name_id = [(key['name'],  key['owner']['id'], key['tracks']['total'], key['id']) \
                    for key in playlists['items']] # Extract the metadata for each song of the playlist
playlist_name_id
playlist_info = pd.DataFrame(playlist_name_id, columns = ["Name", "Owner", "Number_of_tracks", "Tracklist_id"]) # Set the column names for the playlist metadata
playlist_info
playlist_name = "Most Necessary"
playlist_info = playlist_info.set_index('Name')

testPlaylist = playlist(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner, sp)

### Make Dataframe for song features
allSongNames = [song.title for song in testPlaylist.listOfSongs if song.lyrics != " "]
df2  = pd.DataFrame(columns = ["acousticness", "danceability", "tempo", "valence", "energy", "duration_ms"], index = allSongNames)


for song in testPlaylist.listOfSongs:
    if type(song.audioFeatures) == dict:
        df2.loc[song.title] = {k:v for k,v in song.audioFeatures.items() if k in ["acousticness", "danceability", "tempo", "valence", "energy", "duration_ms"]}


df2 = df2.applymap(lambda x: np.float64(x))
df2["duration_s"] = df2["duration_ms"]/1000
df2.drop(["duration_ms"], axis = 1, inplace = True)
df2.mean(axis = 0)


import statsmodels.formula.api as sm


def create_formula(dep_var_name, colList):
    all_columns = "+ ".join([col for col in colList if col != dep_var_name])
    formula = dep_var_name + "~" + all_columns
    return(formula)

dance_formula = create_formula("danceability", df2.columns)

result = sm.ols(formula=dance_formula, data=df2).fit()
result.summary()

##
word_counts = testPlaylist.getWordCounts(min_word_rank= 30)
word_counts.sum(axis = 1)
word_counts.sum(axis = 0).sort_values(ascending = False)

word_counts.head()
df2.head()

df3 = word_counts.join(df2)
df3.head()
df3.shape

dance_formula2 = create_formula("danceability", df3.columns)

result = sm.ols(formula=dance_formula2, data=df3).fit()
result.summary()


















##### 03122018 ####
vect = CountVectorizer(max_features=100)
vectWordFreq = vect.fit_transform(testPlaylist.songLyricsList).toarray()
vectNames = vect.get_feature_names()
vectdf = pd.DataFrame(vectWordFreq,columns = vectNames, index=testPlaylist.songNames)

df3 = df2.join(vectdf)
df3.shape
