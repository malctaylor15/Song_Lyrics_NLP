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

import get_playlist
reload(get_playlist)
from get_playlist import get_playlist

import playlist
reload(playlist)
from playlist import playlist

import utils_adv
reload(utils_adv)
from utils_adv import *

from scipy.spatial.distance import cosine


# Get user playlist information from spotify
testPlaylist = get_playlist("malchemist02", "Kanye West – The Life Of Pablo")

######## 05172018

type(testPlaylist)
dir(testPlaylist)

# Get word frequency of top 300 words
word_freq = testPlaylist.getWordCounts(100)

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
glove_filepath = "/home/owner/Downloads/glove.6B.50d.txt"

os.path.isfile(glove_filepath)
embed_dict = get_word_embeddings(glove_filepath, top_words)

# Validate embeddings
len(embed_dict)
set(list(embed_dict)).symmetric_difference(top_words)
#list(embed_dict.keys())

# Turn embeddings into dictionary
embed_pd = pd.DataFrame(embed_dict).T
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
check_word = "night"
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

####################
### Begin Tsnee ####
####################



from sklearn.manifold import TSNE
# norm_song_embeds.to_csv("EmbedsForPabloKanye.csv")

y1 = [x for x in range(0,10)]
y1[:3]

new_embeds = TSNE(perplexity = 5, random_state=1).fit_transform(norm_song_embeds)
new_embeds = pd.DataFrame(new_embeds, index = norm_song_embeds.index)
plt.ioff()

import utils_adv
reload(utils_adv)
from utils_adv import *
%matplotlib inline

# df1 = find_outliers(new_embeds, n_cluster = 2, numb_pts_to_label=1)

# Run plotting lines all together
fig, ax = plt.subplots()
plot_TSNE_all_labels(ax, new_embeds)
fig.show()
fig.savefig("Life of Pablo All pts Labeled.png")

fig, ax = plt.subplots()
df1 = find_outliers(new_embeds)
plot_TSNE_cluster_overlay(ax, new_embeds, df1)
fig.show()
fig.savefig("Life of Pablo Cluster pts.png")


tsnes = plot_4_TSNE(norm_song_embeds)
outputs = plot_4_TSNE_w_overlay(norm_song_embeds)
