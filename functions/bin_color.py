import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cluster_data as cld
from skimage.measure import regionprops
# from cluster_data import plot_colors

# colorIm = cm.PuRd(np.arange(256))
# print(colorIm[None, :, :-1].shape)
# plot_colors(colorIm[None, :, :-1])
#
# plt.show()


def bin_colors(im, bin_per_axis=4):
    bpa = bin_per_axis
    labels = np.arange(bpa**3) + 1
    labels = labels.reshape((bpa, bpa, bpa))
    print(labels.shape)
    w, h, d = OG_shape = im.shape
    im_array = np.reshape(im, (w * h, d))
    im_ind = (im_array * (bpa-1)).astype('int')
    print(im_ind.shape)
    labeled_im = np.array([labels[i, j, k] for i, j, k in im_ind])
    labeled_im = labeled_im.reshape((w, h))
    plt.figure()
    plt.imshow(labeled_im, cmap='viridis')


def find_dom_color(im, pltcolor=False):
    recon_im, label_im = cld.cluster_colorspace_km(im, n_clusters=2,
                                                   train_size=2000)
    if pltcolor is True:
        cld.plot_colors(recon_im, title_text='k=2 colors from find_dom_color')
        plt.figure()
        plt.imshow(label_im, cmap='viridis')
        plt.suptitle('label im from find_dom_color')
    regions = regionprops(label_im)
    areas, labels = np.split(np.array([[i.area, i.label] for i in regions]),
                             2, axis=1)
    return label_im == labels[np.argmax(areas)]


if __name__ == '__main__':
    print('called')
