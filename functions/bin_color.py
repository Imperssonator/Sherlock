import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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


if __name__ == '__main__':
    print('called')
