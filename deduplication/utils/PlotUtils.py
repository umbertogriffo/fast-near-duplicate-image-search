import os
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


class PlotUtils(object):

    @staticmethod
    def plot_region(df, x0, x1, y0, y1, text=True):
        """
        Plot the region of the mapping space bounded by the given x and y limits.
        """
        FS = (10, 8)
        fig, ax = plt.subplots(figsize=FS)
        pts = df[
            (df.x >= x0) & (df.x <= x1)
            & (df.y >= y0) & (df.y <= y1)
            ]
        ax.scatter(pts.x, pts.y, alpha=.6)
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
        if text:
            texts = []
            for label, x, y in zip(pts.short_file.values, pts.x.values, pts.y.values):
                t = ax.annotate(label, xy=(x, y))
                texts.append(t)
        return ax

    @staticmethod
    def plot_region_around(df, title, margin=5, **kwargs):
        """
        Plot the region of the mapping space in the neighbourhood of the image with
        the given name. The margin parameter controls the size of the neighbourhood around the image.
        """
        xmargin = ymargin = margin
        match = df[df.short_file == title]
        assert len(match) == 1
        row = match.iloc[0]
        return PlotUtils.plot_region(df, row.x - xmargin, row.x + xmargin, row.y - ymargin, row.y + ymargin, **kwargs)

    @staticmethod
    def plot_images_cluster(df, embs, output_path, width = 4000, height = 3000, max_dim = 100):
        """
        Plot the images cluster.
        :param df:
        :param embs: tsne embeddings, an array of unnormalized 2d points.
        :return:
        """

        # The variable tsne contains an array of unnormalized 2d points, corresponding to the embedding.
        # We normalize the embedding so that lies entirely in the range (0,1).
        tx, ty = embs[:, 0], embs[:, 1]
        tx = (tx - np.min(tx)) / (np.max(tx) - np.min(tx))
        ty = (ty - np.min(ty)) / (np.max(ty) - np.min(ty))
        full_image = Image.new('RGBA', (width, height))
        # Finally, we will compose a new RGB image where the set of images have been drawn according to the t-SNE
        # results. Adjust width and height to set the size in pixels of the full image, and set max_dim to
        # the pixel size (on the largest size) to scale images to.
        for img, x, y in zip(df['file'].values, tx, ty):
            tile = Image.open(img)
            rs = max(1, tile.width / max_dim, tile.height / max_dim)
            tile = tile.resize((int(tile.width / rs), int(tile.height / rs)), Image.ANTIALIAS)
            full_image.paste(tile, (int((width - max_dim) * x), int((height - max_dim) * y)), mask=tile.convert('RGBA'))

        full_image.show()
        full_image.save(os.path.join(output_path,"cluster.png"),"PNG")
        resized_image = full_image.resize((int(width / 5), int(height / 5)))
        resized_image.save(os.path.join(output_path, "resized_cluster.png"), "PNG")
