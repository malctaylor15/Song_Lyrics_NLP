## Random utility functions



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE


def plot_4_TSNE(data, random_states = [1,2,3,4], perplexity_input = 5):

    """
    Plot multiple TSNE

    """
    # Create 4 TSNEs
    TSNEs = []


    for rnd in random_states:
        TSNE_temp = TSNE(perplexity = perplexity_input, random_state=rnd).fit_transform(data)
        TSNEs.append(TSNE_temp)
        print("Created a TSNE")


    f, ax = plt.subplots(2, 2)

    def plot_TSNE(embeddings, labels, ax):
        ax.scatter(embeddings[:,0], embeddings[:,1])

        for label, x, y in zip(labels, embeddings[:,0], embeddings[:,1]):
            ax.annotate(label, xy = (x,y), xytext = (20,-20),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
