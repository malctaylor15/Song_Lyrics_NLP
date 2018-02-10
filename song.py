
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
