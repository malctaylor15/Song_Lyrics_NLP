
# coding: utf-8

# System utilities
import os
from os import environ
import subprocess
import sys

# Spotify API
import spotipy
import spotipy.util as util

# NLP Libraries
from wordcloud import WordCloud
from textblob import TextBlob
#import gensim.models.word2vec as w2v
from nltk.tokenize import sent_tokenize, word_tokenize
import gensim
import nltk

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# Random
import re
from pprint import pprint as pp

%reload_ext GeniusAPI_MT
import GeniusAPI_MT
from importlib import reload
reload(GeniusAPI_MT)
from GeniusAPI_MT import *

import pandas as pd

# Set environment variables
os.environ['SPOTIPY_CLIENT_ID'] = "d3c68e4eb95942fb9a0ceb508d62c127"
os.environ['SPOTIPY_CLIENT_SECRET'] = "bab6935eaa2f478ea4c47a6c8a96eec8"
os.environ['SPOTIPY_REDIRECT_URI'] = "http://localhost/"

def get_tracklist(tracklist_id, username):
    """
    This function takes a spotify tracklist id and spotify username
    and returns a dictionary where the track name is the key.
    This function interacts with the Spotify API to find information
    for each song of a track list

    Inputs:
        tracklist_id = Spotify tracklist id (string)
        username = spotify username (string)

    Output:
        allTracks = dictionary with song artist and track name

    """
    print("Running get_tracklist...")
    allTracks = {}
    results = sp.user_playlist(username, tracklist_id, fields="tracks")
    tracks = results['tracks']
    for i, item in enumerate(tracks['items']):
        track = item['track']
        trackName = track['name']
        trackArtist = track['artists'][0]['name']
        allTracks[trackName] = trackArtist
    pp(allTracks)
    return allTracks

def get_tracklist_class(tracklist_id, username):
    """
    This function takes a spotify tracklist and spotify username
    and returns a list of the song class.
    This function interacts with the spotify API to find the artist and trackname
    for each song in the playlist and creates a song object for each song.

    Inputs:
        tracklist_id = Spotify tracklist id (string)
        username = spotify username (string)
    Output:
        allTracks = list of song objects in specified playlist (list of song)


    """
    print("Running get_tracklist_class...")
    allTracks = []
    results = sp.user_playlist(username, tracklist_id, fields="tracks")
    tracks = results['tracks']
    for i, item in enumerate(tracks['items']):
        track = item['track']
        song_temp = song(track['name'], track['artists'][0]['name'])
        allTracks.append(song_temp)
    return allTracks

def get_user_playlists_2(username):
    """
    This function finds playlist name, number of tracks and spotify tracklist id
    for a given user name. The spotify tracklist id is used in the gettracklist
    functions

    Input:
        username = spotify number
    Output:
        all_playlistinfo = list containing playlist name, number of tracks and
        the spotify tracklist id for each playlist (list of list)

    """
    print("Running get_user_playlists_2...")
    all_playlist_info = [[playlist["name"], playlist['tracks']['total'], playlist['id']]
                         for playlist in playlists['items']
                         if playlist['owner']['id'] == username]
    return(all_playlist_info)

def get_user_playlists(username):
    print("Running get_user_playlists...")
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print()
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])
            results = sp.user_playlist(username, playlist['id'],
                fields="tracks,next")
            tracks = results['tracks']

def get_tracklist_lyrics(tracklist):
    """
    This function takes a list of song (class) and returns a string of
    the concatentated lyrics for all songs in playlist (list of songs).

    Input:
        tracklist = list of songs

    Output:
        lyrics = concatenated lyrics
    """
    print("Running get_tracklist_lyrics...")
    lyrics = str()
    for song in tracklist:
        if song.lyrics != ():
            lyrics = lyrics + song.lyrics
    return(lyrics)

# Import Genius API functions
#sys.path.append('/Users/board/Desktop/Kaggle/Song_Lyrics_NLP')
currentDirectory = os.getcwd()
sys.path.append(currentDirectory)

"""
lyrics_dict = {}
for song_name, artist in tracklist.items():
    lyrics_dict[song_name] = get_song_lyrics(artist_name=artist, song_title=song_name, headers=headers)

print(lyrics_dict.keys())
"""

class song:
    def __init__(self, title, artist):
        """
        Creates a song object using the title and artist for a song
        This will get the lyrics and create TextBlob object
        """
        print("Instantiating a song...")
        self.title = title
        self.artist = artist
        self.lyrics = get_song_lyrics(self.artist, self.title, headers = headers)
        if self.lyrics == ():
            print("No lyrics found. Not creating TextBlob Object")
        else:
            self.blob = TextBlob(self.lyrics) #initialize the object for TextBlob

    def showWordCloud(self):
        """
        Uses the lyrics to create a WordCloud image and object
        """
        if self.lyrics == ():
            print("No lyrics found")
            return ()
        self.wc = WordCloud().generate(self.lyrics)
        self.wc.to_image().show()

    def getSentiment(self, trace = 0):
        """
        This function uses the lyrics of a song to find the polarity
        using the lyrics as a TextBlob object

        If trace is 1 then it will print the polarity

        Output:
            polarity = polarity of the lyrics of the song (float)
        """

        self.polarity = self.blob.sentiment.polarity
        if trace:
            print("Polarity is ", self.polarity)
        return(self.polarity)

    def getWordCounts(self, numb_words = 200):
        vectorizer = CountVectorizer(analyzer = "word",
                                 tokenizer = None,
                                 preprocessor = None,
                                 stop_words = None,
                                 min_df = 0,
                                 max_features = numb_words)


        train_data_features = vectorizer.fit_transform(self.lyrics)
        vocab = vectorizer.get_feature_names()

        # Sum up the counts of each vocabulary word
        dist = np.sum(train_data_features.toarray(), axis=0)

        # For each, print the vocabulary word and the number of times it
        # appears in the training set
        for tag, count in zip(vocab, dist):
            print (tag, count)

    def getTags(self):
        print(self.blob.tags)

    def getNouns(self):
        print(self.blob.noun_phrases)

class playlist:
    def __init__(self, tracklist_id, username):
        """
        Playlists are defined by a unique spotify playlist id and username

        Creating a playlist class will initialize the list of song (class) and
        concatentate all the lyrics from each song
        """
        print("Instantiating a playlist...")
        self.username = username
        self.tracklist_id = tracklist_id
        self.listOfSongs = get_tracklist_class(self.tracklist_id, self.username)
        self.allLyrics = get_tracklist_lyrics(self.listOfSongs)

    def showWordCloud(self):
        self.wc = WordCloud().generate(self.allLyrics)
        self.wc.to_image().show()

    def getSentimentList(self):
        """
        This function uses the list of song (class) from the playlist
        to aggregate the polarity for each song

        Output:
            self.sentimentList = list of polarity for each song (list of float)

        """

        self.sentimentList = [song.getSentiment() for song in self.listOfSongs]
        return(self.sentimentList)

    def buildWord2Vec(self, num_features = 50, context_size = 7, min_word_count = 4):
        downsampling = 1e-1

        self.songs2vec = w2v.Word2Vec(
            sg=1,
            seed=1234,
            size=num_features,
            min_count=min_word_count,
            window=context_size,
            sample=downsampling
            )
        self.songs2vec.build_vocab(self.allLyrics)
        self.songs2vec.train(corpus, total_examples = self.songs2vec.corpus_count
                , epochs = self.songs2vec.iter)


    def getWordCounts(self, numb_words = 200):
        ### Bag of words functionality
        self.songLyricsList = [song.lyrics for song in self.listOfSongs]
        self.songNames = [song.title for song in self.listOfSongs]
        #del songNames[0] delete later if not needed
        #del self.songLyricsList[0]  delete later if not needed
        vect = CountVectorizer()
        vectWordFreq = vect.fit_transform(self.songLyricsList).toarray()
        self.vectNames = vect.get_feature_names()
        self.vectdf = pd.DataFrame(vectWordFreq,columns = self.vectNames, index=self.songNames)
        return self.vectdf

    def getTfidf(self):
        self.wordFrequency = self.getWordCounts() #copied from elswhere
        transformer = TfidfTransformer(smooth_idf=False)
        tfidf = transformer.fit_transform(self.wordFrequency.values)
        self.tfidf_df = pd.DataFrame(tfidf.toarray(),columns = self.vectNames, index=self.songNames)
        return self.tfidf_df

# ## Let's get it running

# Get user playlist information from spotify
username = '1282829978'  #TODO: Make user input
scope = 'user-library-read playlist-read-private user-top-read' #the permissions to give our application
token = util.prompt_for_user_token(username,scope)
sp = spotipy.Spotify(auth=token)
playlists = sp.user_playlists(username)

# Look at user playlist name, number of tracks, and spotify tracklist id
playlists_info = get_user_playlists_2(username)
pp(playlists_info)

playlist_index = 1 # Which playlist index to use
spotify_tracklist_id = playlists_info[playlist_index][2]
tracklist = get_tracklist_class(spotify_tracklist_id, username) # Look at songs in playlist

#############################################
#### Begin Testing class functionalities ####
#############################################

### Song Object Functionality ###
testSong = song('Rap God', 'Eminem') #instantiate a song class object
testSong.getSentiment()
testSong.showWordCloud()
print(testSong.polarity) # Same as getSentiment() ?

##############################
### test the lemmatization 20180130 ###
##############################
"""lyricsBeforeAndAfter  =
for lyricsBeforeAndAfter in this:
    if lyricsBeforeAndAfter[0] != lyricsBeforeAndAfter[1]:
        print(lyricsBeforeAndAfter)"""

###############################

### Testing word counting after lemmatization is done 20180130 ###
testSongTokenized = word_tokenize(testSong.lyrics)
counter = Counter(testSongTokenized)
counter.most_common(15)

############################################################

### Testing playlist class object funcitonality

testPlaylist = playlist(spotify_tracklist_id, username)

testPlaylist.getTfidf()
wordFrequency = testPlaylist.getWordCounts()
wordFrequency

### Get the words showing in all the songs of a playlist ### 20180129
songList = testPlaylist.getTfidf().drop("F**kin' Problems",axis=0)
songList.T[songList.apply(lambda col: col.all((0)),axis=0)]

# New list of strings with song lyrics (untested)

"""
songs2vec = w2v.Word2Vec(
    sg=1,
    seed=1234,
    size=20,
    min_count=4,
    window=7,
    sample=1e-1
    )

songs2vec.build_vocab(corpus)
songs2vec.corpus_count
songs2vec.train(corpus, total_examples = songs2vec.corpus_count
                , epochs = songs2vec.iter)

songs2vec.most_similar('rainbow')
songs2vec.most_similar('cry')
songs2vec.similarity('rainbow', 'cry')"""

#wc1 = WordCloud().generate(wc_corpus)
#wc1.to_image().show()






####################################
### Testing nltk 20180126 -Devin ###
####################################

from nltk.corpus import stopwords
nltk.download_shell() # Downloads the corpus using a shell
stopwords.words('english') # These are commonly used words with little useful meaning
from nltk.corpus import brown # Importing Brown University corpus
#brown.sents(categories=['news', 'editorial']) # Sentences from periodical text
words = [word for word in brown.words(categories=['news', 'editorial']) if word.lower() not in stopwords.words('english')]
brown.sents(categories=['news'])[0]
words

################################################################################################

from collections import Counter
import pandas as pd
import numpy as np

counter  = Counter(cleanWords)

counter.most_common(150)

np.mean([x for x in counter.values()])
np.median([x for x in counter.values()])

### One possible preprocessing implementation, but probaly wont be used, just observed while building our own

import string
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re

def preprocess(sentence):
	sentence = sentence.lower()
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(sentence)
	filtered_words = [w for w in tokens if not w in stopwords.words('english')]
	return " ".join(filtered_words)

sentence = "At eight o'clock on Thursday morning Arthur didn't feel very good. French-Fries" # Example
print(preprocess(sentence)) # Example

sentence1 = []
cleanWords2 = []
for sentence in brown.sents(categories='news'):
    for word in sentence:
        sentence1.append(word)

for word in sentence1:
    cleanWords2.append(preprocess(word))

cleanWords2 = list(filter(None, cleanWords2))
cleanWords2

counter = Counter(cleanWords2)
counter.most_common(15)
sentence1
