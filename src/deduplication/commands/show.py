import os

from sklearn.manifold import TSNE

from deduplication.utils.PlotUtils import PlotUtils


def show(df_dataset,
         output_path):
    """
    Generating a t-SNE (t-distributed Stochastic Neighbor Embedding) of a set of images, using a feature vector for
    each image derived from the pHash function.
    :param df_dataset:
    :param images_path:
    :param output_path:
    :param hash_algo:
    :param hash_size:
    :param parallel:
    :param batch_size:
    :return:
    """

    hash_str_len = len(df_dataset.at[0, 'hash_list'])

    # The default of 1,000 iterations gives fine results, but I'm training for longer just to eke
    # out some marginal improvements. NB: This takes almost an hour!
    tsne = TSNE(random_state=1, n_iter=15000, metric="cosine")

    embs = tsne.fit_transform(df_dataset[[str(i) for i in range(0, hash_str_len)]])

    # Add to dataframe for convenience
    df_dataset['x'] = embs[:, 0]
    df_dataset['y'] = embs[:, 1]

    # Save a copy of our t-SNE mapping data for later use
    df_dataset.to_csv(os.path.join(output_path, 'images_tsne.csv'))

    PlotUtils.plot_images_cluster(df_dataset, embs, output_path, width=4000, height=3000, max_dim=100)
    # TODO: image neigbours
    # PlotUtils.plot_region_around(df_dataset_in, '2018-12-11-15-031193.png')
    # plt.show()
