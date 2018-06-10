# System utilities
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
%matplotlib inline

# Spotify API
#nltk.download("stopwords")
#nltk.download("wordnet")
#nltk.download("punkt")

# Word embeddings
# https://nlp.stanford.edu/projects/glove/

from importlib import reload

from Word_Embeddings_Related import get_playlist

reload(get_playlist)
from Word_Embeddings_Related.get_playlist import get_playlist

import playlist
reload(playlist)

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

os.getcwd()
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
dep_var2 = song_cosine_dict["30 Hours"]

dep_var2.head()
norm_song_embeds.head()

# Create embedding dataframe
dep_embedding = pd.concat([dep_var2, norm_song_embeds], axis = 1)
dep_embedding.rename(columns = {0:"song_cosine"}, inplace = True)

# Create words DataFrame
dep_words = pd.concat([dep_var2, word_freq], axis = 1)
dep_words.rename(columns = {0:"song_cosine"}, inplace = True)


X_sc_em =  dep_embedding.drop(["song_cosine"], axis = 1)
Y_sc_em = dep_embedding["song_cosine"]

X_train, X_test, y_train, y_test = train_test_split(X_sc_em, Y_sc_em)

fit1 = LinearRegression().fit(X_train, y_train)
fit1.score(X_test, y_test)

X_sc_nw =  dep_words.drop(["song_cosine"], axis = 1)
Y_sc_nw = dep_words["song_cosine"]

X_train, X_test, y_train, y_test = train_test_split(X_sc_nw, Y_sc_nw)
fit1 = LinearRegression().fit(X_train, y_train)
fit1.score(X_test, y_test)

## Naturally the embeddings perform better in this case because they were used
# In a non linear fashion in creating the depednent

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
plt.scatter(new_embeds.iloc[:,0], new_embeds.iloc[:,1])

for label, x, y in zip(norm_song_embeds.index.values, new_embeds.iloc[:,0], new_embeds.iloc[:,1]):
    plt.annotate(label, xy = (x,y), xytext = (20,-20),
    textcoords='offset points', ha='right', va='bottom',
    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
    arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

plt.show()



from sklearn.cluster import KMeans

n_cluster = 3

cluster_fit = KMeans(n_clusters = n_cluster, random_state=2).fit(new_embeds)

# Combine label and center
unique_labels = np.sort(np.unique(cluster_fit.labels_))
centers = cluster_fit.cluster_centers_
cl_center_dict = {label:center for label, center in zip(unique_labels, centers)}

# Initalize dict for storing distances
# center_dist = {label: [] for label in cluster_fit.labels_}
# TODO: make key of center dist a dataframe
center_dist = {label: pd.DataFrame(columns = ["Distance"]) for label in cluster_fit.labels_}


from scipy.spatial.distance import euclidean

# take in pt, cluster center, song name
for pt, cl_label,song_name in zip(new_embeds.values, cluster_fit.labels_, new_embeds.index.tolist()):

    pt_center = cl_center_dict[cl_label]
    dist_from_center = euclidean(pt, pt_center)
    # center_dist[cl_label].append((song_name, dist_from_center))

    center_dist[cl_label].loc[song_name]= dist_from_center

numb_pts_to_label = 3 # Name top n farthest/closest points from their center
pts_to_label = pd.DataFrame(columns = ["Distance", "Center"])
for center_lbl in unique_labels:
    top_pts_far = center_dist[center_lbl].sort_values(by="Distance", ascending = False)[:3]
    top_pts_far["Center"] = center_lbl
    top_pts_near = center_dist[center_lbl].sort_values(by="Distance", ascending = False)[:-3]

    pts_to_label = pd.concat([pts_to_label, top_pts_far], axis = 0)
type(top_pts_far)

pts_to_label = pts_to_label.join(new_embeds)

plt.scatter(centers[:,0], centers[:,1], color = "red")
plt.scatter(new_embeds.iloc[:,0], new_embeds.iloc[:,1])

for label, x, y in zip(pts_to_label.index.tolist(), pts_to_label[0], pts_to_label[1]):
    plt.annotate(label, xy = (x,y), xytext = (20,-20),
    textcoords='offset points', ha='right', va='bottom',
    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
    arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

plt.show()



#################################
#################################
#################################


# Name top n farthest/closest points from their center
pts_to_label = pd.DataFrame(columns = ["Distance", "Close_Far", "Label"])
for center_lbl in unique_labels:
    sorted_pts = center_dist[center_lbl].sort_values(by="Distance", ascending = False)
    # Points far away
    top_pts_far = sorted_pts[:numb_pts_to_label]
    top_pts_far["Close_Far"] = "F"
    # Points closer
    top_pts_near = sorted_pts[-numb_pts_to_label:]
    top_pts_near.loc[:,"Close_Far"] = "C"
    # Combine and add Label
    pts = top_pts_far.append(top_pts_near).copy()
    pts.loc[:,"Label"] = np.repeat(center_lbl, pts.shape[0])

    pts_to_label = pd.concat([pts_to_label, pts], axis = 0)

data = new_embeds
pts_to_label = pts_to_label.join(data)

for center, label in zip(centers, unique_labels):
    # pts_to_label.loc["Center"+str(label)] = {"Distance":0, "Close_Far":"CC", "Label":label, 0:center}
    temp_array = [0, "CC", label]
    for x in center:
        temp_array.append(x)
    pts_to_label.loc["Center"+str(label)] = temp_array
pts_to_label

center_info
unique_labels
cluster_fit.cluster_centers_


import utils_adv
reload(utils_adv)
from utils_adv import *


df1 = find_outliers(new_embeds)

plot_TSNE_all_labels(new_embeds, title="Life of Pablo TSNE Embeddings")
