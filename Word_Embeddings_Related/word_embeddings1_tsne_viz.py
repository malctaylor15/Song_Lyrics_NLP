import pandas as pd
from sklearn.manifold import TSNE
from importlib import reload
import utils_adv
reload(utils_adv)
from utils_adv import *
# %matplotlib inline
#plt.ioff()

def TSNE(norm_song_embeds):
    new_embeds = TSNE(perplexity = 5, random_state=1).fit_transform(norm_song_embeds)
    new_embeds = pd.DataFrame(new_embeds, index = norm_song_embeds.index)

    # df1 = find_outliers(new_embeds, n_cluster = 2, numb_pts_to_label=1)

    # Run plotting lines all together
    fig, ax = plt.subplots()
    plot_TSNE_all_labels(ax, new_embeds)
    fig.show()
    fig.savefig("../TSNE_Plots/Life of Pablo All pts Labeled.png")

    fig, ax = plt.subplots()
    df1 = find_outliers(new_embeds)
    plot_TSNE_cluster_overlay(ax, new_embeds, df1)
    fig.show()
    fig.savefig("../TSNE_Plots/Life of Pablo Cluster pts.png")

    tsnes = plot_4_TSNE(norm_song_embeds)
    outputs = plot_4_TSNE_w_overlay(norm_song_embeds)
