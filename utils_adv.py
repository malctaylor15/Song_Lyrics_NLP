## Random utility functions



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean

import os


# Read in the embeddings from the top words list
def get_word_embeddings(glove_path, words, output_freq = 10000, cutoff = None):
    """
    Look in embeddings file and get the matching embeddings

    For each line in the file path, split on spaces and see if the word
    is in the words list

    Inputs:
        glove_path (str): path to embeddings
        words (list): list of words to retrieve from embeddings file
        output_freq (int) : number of words to alert after going through embeddings file
        cutoff (int): how many lines in embeddings to look through (debugging)
    Output:
        embed_dict (dict): keys are word name, value is list of the embeddings
    """

    if not os.path.isfile(glove_path): raise ValueError("Glove file not found: path={}".format(glove_path))

    with open(glove_path, 'r+', encoding='utf-8') as fp:
        i = 0
        embed_dict = {}
        for line in fp:
            split_line = line.split()
            if split_line[0] in words:
                embed_dict[split_line[0]] = split_line[0:]
            i +=1
            if i % output_freq ==0 :
                print("Looked through ", i, " words")
            if i == cutoff: break
            if len(embed_dict) == len(words): break

    return(embed_dict)




def find_outliers(data, n_cluster = 3, numb_pts_to_label = 3, rnd_state=4):
    """
    Uses k means to find clusters and returns a dataframe with
    the center, points, near and far from the center

    """

    cluster_fit = KMeans(n_clusters = n_cluster, random_state=rnd_state).fit(data)

    # Combine label and center
    unique_labels = np.sort(np.unique(cluster_fit.labels_))
    centers = cluster_fit.cluster_centers_
    cl_center_dict = {label:center for label, center in zip(unique_labels, centers)}

    # Get distance for each point in the cluster to the center
    center_dist = {label: pd.DataFrame(columns = ["Distance"]) for label in cluster_fit.labels_}

    # take in pt, cluster center, song name
    for pt, cl_label,song_name in zip(data.values, cluster_fit.labels_, data.index.tolist()):
        pt_center = cl_center_dict[cl_label]
        dist_from_center = euclidean(pt, pt_center)

        center_dist[cl_label].loc[song_name]= dist_from_center
        # Do you want to store embeddings here too?

    # Name top n farthest/closest points from their center
# Name top n farthest/closest points from their center
    pts_to_label = pd.DataFrame(columns = ["Distance", "Close_Far", "Label"])
    for center_lbl in unique_labels:
        sorted_pts = center_dist[center_lbl].sort_values(by="Distance", ascending = False)
        # Points far away
        top_pts_far = sorted_pts[:numb_pts_to_label].copy()
        top_pts_far.loc[:,"Close_Far"] = "F"
        # Points closer
        top_pts_near = sorted_pts[-numb_pts_to_label:].copy()
        top_pts_near.loc[:,"Close_Far"] = "C"
        # Combine and add Label
        pts = top_pts_far.append(top_pts_near)
        pts.loc[:,"Label"] = np.repeat(center_lbl, pts.shape[0])
        # Combine this cluster with the rest
        pts_to_label = pd.concat([pts_to_label, pts], axis = 0)

    # Add embeddings to dataframe
    pts_to_label = pts_to_label.join(data)

    # Append centers to dataframe
    for center, label in zip(centers, unique_labels):
        # pts_to_label.loc["Center"+str(label)] = {"Distance":0, "Close_Far":"CC", "Label":label, 0:center}
        temp_array = [0, "CC", label]
        for x in center:
            temp_array.append(x)
        pts_to_label.loc["Center"+str(label)] = temp_array

    return(pts_to_label)



def plot_TSNE_all_labels(ax, embeddings, title= "TSNE Embeddings"):
    # f, ax = plt.subplots(2, 2)
    ax.scatter(embeddings.iloc[:,0], embeddings.iloc[:,1])
    ax.set_xlabel("TSNE Embedding Dimension 1")
    ax.set_ylabel("TSNE Embedding Dimension 2")
    ax.set_title(title)

    # Annotate points
    for label, x, y in zip(embeddings.index.tolist(), embeddings.iloc[:,0], embeddings.iloc[:,1]):
        ax.annotate(label, xy = (x,y), xytext = (20,-20),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

    # Save picture?
    #if save_fig: ax.savefig(title+".png")
    #if show_fig: ax.show()
    #ax.close()

def plot_TSNE_cluster_overlay(ax, embeddings, cluster_info, title_start = "TSNE Embeddings"):
    pts = ax.scatter(embeddings.iloc[:,0], embeddings.iloc[:,1], color = "blue", label="Reg Points")
    ax.set_xlabel("TSNE Embedding Dimension 1")
    ax.set_ylabel("TSNE Embedding Dimension 2")
    n_cluster_str = str(max(cluster_info["Label"])+1)
    title = title_start + "\nwith Cluster Overlay (k="+n_cluster_str+")"
    ax.set_title(title)

    # Annotate the points close and far to the cluster centers
    cluster_x = cluster_info[cluster_info["Close_Far"] != "CC"][0]
    cluster_y = cluster_info[cluster_info["Close_Far"] != "CC"][1]
    for label, x, y in zip(cluster_x.index.tolist(), cluster_x, cluster_y):
        ax.annotate(label, xy = (x,y), xytext = (20,-20),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
    outliers = ax.scatter(cluster_x, cluster_y, color = 'green', label="Close and Far")

    # Annotate the points close and far to the cluster centers
    cluster_c_x = cluster_info[cluster_info["Close_Far"] == "CC"][0]
    cluster_c_y = cluster_info[cluster_info["Close_Far"] == "CC"][1]
    for label, x, y in zip(cluster_c_x.index.tolist(), cluster_c_x, cluster_c_y):
        ax.annotate(label, xy = (x,y), xytext = (20,-20),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
    centers = ax.scatter(cluster_c_x, cluster_c_y, color = 'red', label="Centers")

    ax.legend(handles = [pts, outliers, centers], loc="best")

    #if show_fig: ax.show()
    #if save_fig: ax.savefig(title_start+"k_{}.png".format(n_clusters_str))
    #ax.close()




def plot_4_TSNE(data, random_states = [1,2,3,4], perplexity_input = 5):

    """
    Plot multiple TSNE

    """
    # Create 4 TSNE Embeddings
    TSNEs = []
    for rnd in random_states:
        TSNE_temp = TSNE(perplexity = perplexity_input, random_state=rnd).fit_transform(data)
        embed_pd = pd.DataFrame(TSNE_temp, index = data.index)
        TSNEs.append(embed_pd)
    print("Created a TSNEs")

    # Plot different embeddings in one image
    n_rows = int(np.ceil(len(random_states)/2))
    f,axs = plt.subplots(nrows= n_rows, ncols = 2, figsize = (10,10))
    #Unroll axs
    unroll_ax = [ax for ax1 in axs for ax in ax1]
    for tsne,ax, rnd in zip(TSNEs, unroll_ax, random_states):
        plot_TSNE_all_labels(ax, tsne)

    print("Finished plotting all TSNEs")

    debug_dict = {"TSNEs": TSNEs, "figure": f}
    return(debug_dict)



def plot_4_TSNE_w_overlay(data, random_states = [1,2,3,4], perplexity_input = 5, n_cluster = 2, pts_to_label = 2, fig_size= (10,10)):

    """
    Plot multiple TSNE

    """
    # Create 4 TSNE Embeddings
    TSNEs = []
    for rnd in random_states:
        TSNE_temp = TSNE(perplexity = perplexity_input, random_state=rnd).fit_transform(data)
        embed_pd = pd.DataFrame(TSNE_temp, index = data.index)
        TSNEs.append(embed_pd)
    print("Created TSNEs")

    # Find outlier points
    outlier_dfs = []
    for tsne, rnd in zip(TSNEs, random_states):
        outlier_df = find_outliers(tsne, rnd_state=rnd)
        outlier_dfs.append(outlier_df)
    print("Found outlier dfs")

    # Plot
    n_rows = int(np.ceil(len(random_states)/2))
    f,axs = plt.subplots(nrows= n_rows, ncols = 2, figsize = fig_size)
    unroll_ax = [ax for ax1 in axs for ax in ax1]
    for tsne, outlier_df, ax in zip(TSNEs, outlier_dfs, unroll_ax):
        plot_TSNE_cluster_overlay(ax, tsne, outlier_df)
    plt.tight_layout()
    print("Created outlier image")

    # Debug outputs
    debug_dict = {"TSNEs": TSNEs, "outlier_df": outlier_dfs, "figure":f}
    return(debug_dict)
