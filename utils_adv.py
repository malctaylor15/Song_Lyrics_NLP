## Random utility functions



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean



def find_outliers(data, n_cluster = 3, numb_pts_to_label = 3):
    """
    Uses k means to find clusters and returns a dataframe with
    the center, points, near and far from the center

    """

    cluster_fit = KMeans(n_clusters = n_cluster, random_state=2).fit(data)

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
        top_pts_far = sorted_pts[:numb_pts_to_label]
        top_pts_far.loc[:,"Close_Far"] = "F"
        # Points closer
        top_pts_near = sorted_pts[-numb_pts_to_label:]
        top_pts_near.loc[:,"Close_Far"] = "C"
        # Combine and add Label
        pts = top_pts_far.append(top_pts_near).copy()
        pts.loc[:,"Label"] = np.repeat(center_lbl, pts.shape[0])

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



def plot_TSNE_all_labels(embeddings, title= "TSNE Embeddings"):
    # f, ax = plt.subplots(2, 2)
    plt.scatter(embeddings.iloc[:,0], embeddings.iloc[:,1])
    plt.xlabel("TSNE Embedding Dimension 1")
    plt.ylabel("TSNE Embedding Dimension 2")
    plt.title(title)
    for label, x, y in zip(embeddings.index.tolist(), embeddings.iloc[:,0], embeddings.iloc[:,1]):
        plt.annotate(label, xy = (x,y), xytext = (20,-20),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
    plt.savefig(title+".png")
    plt.show()
    plt.close()


def plot_4_TSNE(data, random_states = [1,2,3,4], perplexity_input = 5):

    """
    Plot multiple TSNE

    """
    # Create 4 TSNEs
    TSNEs = []

    # f, ax = plt.subplots(2, 2)

    for rnd in random_states:
        TSNE_temp = TSNE(perplexity = perplexity_input, random_state=rnd).fit_transform(data)
        TSNEs.append(TSNE_temp)
        print("Created a TSNE")
