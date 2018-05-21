
from wordcloud import WordCloud
from textblob import TextBlob

from importlib import reload
import GeniusAPI_MT
reload(GeniusAPI_MT)
from GeniusAPI_MT import *

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import numpy as np
import pandas as pd


class song:
    def __init__(self, title, artist, **kwargs):
        """
        Creates a song object using the title and artist for a song
        This will get the lyrics and create TextBlob object
        """
        #print("Instantiating a song...") # For testing
        self.title = title
        self.artist = artist
        self.lyrics = get_song_lyrics(self.artist, self.title, headers = headers)
        keywords_for_spotifyid = ["spotify_id", "sp"]

        if all([x in kwargs.keys() for x in keywords_for_spotifyid]):
            sp = kwargs["sp"]
            spotify_id = kwargs["spotify_id"]
            #print("Found ", title, " by ", artist, ". It has a spotify id")

            self.audioFeatures = sp.audio_features(spotify_id)[0]



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

    def getWordCounts(self):
        """
        Counts the number of times a word is in a song
        """
        vectorizer = CountVectorizer()
        feats = vectorizer.fit_transform([self.lyrics]).toarray()[0]
        vocab = vectorizer.get_feature_names()

        word_counts = pd.Series(feats, index = vocab).T.sort_values(ascending = False)

        return(word_counts)



    def getTags(self):
        print(self.blob.tags)

    def getNouns(self):
        print(self.blob.noun_phrases)
