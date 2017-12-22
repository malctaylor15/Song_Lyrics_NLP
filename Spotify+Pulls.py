
# coding: utf-8

# In[ ]:

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
import gensim.models.word2vec as w2v
from nltk.tokenize import sent_tokenize, word_tokenize
import gensim


# Random 
import re 
from pprint import pprint as pp

# Set environment variables 
os.environ['SPOTIPY_CLIENT_ID'] = "d3c68e4eb95942fb9a0ceb508d62c127"
os.environ['SPOTIPY_CLIENT_SECRET'] = "bab6935eaa2f478ea4c47a6c8a96eec8"
os.environ['SPOTIPY_REDIRECT_URI'] = "http://localhost/"


# In[ ]:

def get_tracklist(tracklist_id, username):
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

# In[ ]:

def get_tracklist_class(tracklist_id, username):
    allTracks = []
    results = sp.user_playlist(username, tracklist_id, fields="tracks")
    tracks = results['tracks']
    for i, item in enumerate(tracks['items']):
        track = item['track']
        song_temp = song(track['name'], track['artists'][0]['name'])
        allTracks.append(song_temp)
    return allTracks

# In[ ]:

def get_user_playlists_2(username):
    all_playlist_info = [[playlist["name"], playlist['tracks']['total'], playlist['id']] 
                         for playlist in playlists['items'] 
                         if playlist['owner']['id'] == username]
    return(all_playlist_info)


# In[ ]:

def get_user_playlists(username): 
    
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print()
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])
            results = sp.user_playlist(username, playlist['id'],
                fields="tracks,next")
            tracks = results['tracks']

# In[]:
def get_tracklist_lyrics(tracklist):
    lyrics = str()
    for song in tracklist:
        if song.lyrics != ():
            lyrics = lyrics + song.lyrics
    return(lyrics)


# ## Let's get it running 
# In[ ]:

username = '1282829978'  #TODO: Make user input
scope = 'user-library-read playlist-read-private user-top-read'
token = util.prompt_for_user_token(username,scope)
sp = spotipy.Spotify(auth=token)
playlists = sp.user_playlists(username)


# In[ ]:
playlists_info = get_user_playlists_2(username)
pp(playlists_info)
# In[ ]:
playlist_index = 1
spotify_tracklist_id = playlists_info[playlist_index][2]
tracklist = get_tracklist(spotify_tracklist_id, username)

# In[ ]:

# The location of genius API_MT
#sys.path.append('/Users/board/Desktop/Kaggle/Song_Lyrics_NLP')
currentDirectory = os.getcwd()
sys.path.append(currentDirectory)
from GeniusAPI_MT import *


# In[ ]:
"""
lyrics_dict = {}
for song_name, artist in tracklist.items():
    lyrics_dict[song_name] = get_song_lyrics(artist_name=artist, song_title=song_name, headers=headers)

print(lyrics_dict.keys())
"""
# In[ ]:

class song: 
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        self.lyrics = get_song_lyrics(self.artist, self.title, headers = headers)
        self.blob = TextBlob(self.lyrics) #initialize the object for TextBlob
        
    def showWordCloud(self):
        if self.lyrics == ():
            print("No lyrics found")
            return ()
        self.wc = WordCloud().generate(self.lyrics)
        self.wc.to_image().show()
        
    def getSentiment(self, trace = 0):
        self.polarity = self.blob.sentiment.polarity
        if trace:
            print("Polarity is ", self.polarity)
        return(self.polarity)
        
    def getTags(self):
        print(self.blob.tags)
    def getNouns(self):
        print(self.blob.noun_phrases)

# In[ ]:

class playlist:
    def __init__(self, tracklist_id, username):
        self.username = username
        self.tracklist_id = tracklist_id
        self.listOfSongs = get_tracklist_class(self.tracklist_id, self.username)
        self.allLyrics = get_tracklist_lyrics(self.listOfSongs)
        
    def showWordCloud(self):
        self.wc = WordCloud().generate(self.allLyrics)
        self.wc.to_image().show()
    
    def getSentimentList(self):
        self.sentimentList = [song.getSentiment() for song in self.listOfSongs]
        return(self.sentimentList)
        
    def buildWord2Vec(self, num_features = 50, context_size = 7, min_word_count = 1):
        corpus = [song.lyrics for song in self.listOfSongs]
        downsampling = 1e-1
        
        songs2vec = w2v.Word2Vec(
            sg=1,
            seed=1234,
            size=num_features,
            min_count=min_word_count,
            window=context_size,
            sample=downsampling
            )
        songs2vec.build_vocab(corpus)
    


# In[ ]:
        
### Testing the object functionality
testSong = song('Rap God', 'Eminem')
testSong.getSentiment()

# In[ ]:

testSong.showWordCloud()
print(testSong.polarity)

# In[ ]: 

testPlaylist = playlist(spotify_tracklist_id, username)

# In[ ]: 

songlist = testPlaylist.listOfSongs
corpus = []
wc_corpus = str()
for song in songlist:
    words = song.lyrics.lower().split()
    for word in words:
        corpus.append(words)
        wc_corpus = wc_corpus + ' ' + word
# In [9]:
print(len(corpus))
print(len(wc_corpus))

# In[ ]:
songs2vec = w2v.Word2Vec(
    sg=1,
    seed=1234,
    size=20,
    min_count=1,
    window=7,
    sample=1e-1
    )

songs2vec.build_vocab(corpus)
songs2vec.corpus_count
songs2vec.train(corpus, total_examples = songs2vec.corpus_count
                , epochs = songs2vec.iter)

songs2vec.most_similar('vibe')

wc1 = WordCloud().generate(wc_corpus) 
wc1.to_image().show()


# In[ ]:
def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist,wordfreq))


# In[ ]:
wordListToFreqDict(corpus[1])
# In[ ]:

# In[ ]:



# In[ ]:
    
"""Playlist1 = playlist(playlists_info[playlist_index][2], username)
    
# Helpful code from Kaggle
#articles_tokens.append([word for word in word_tokenize(str(df["text"][i].lower())) if len(word)>2])
model = gensim.models.Word2Vec(articles_tokens, min_count=5,size=100,workers=4)
model.wv.most_similar("lula")
model.wv.most_similar("propina")


In [10]:


# In[ ]:
Playlist1.showWordCloud()

# In[]:
demo = Playlist1.tracklist[4]
print(demo.lyrics)
wc = WordCloud().process_text(demo.lyrics)  
print(wc)


# In[]:
#print(len(Playlist1.allLyrics))
#print(len(demo.lyrics))
"""

# In[]:


