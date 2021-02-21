import numpy as np
import os
import skimage.io as io
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import skimage.filters as flt
import skimage.morphology as mph
import scipy.ndimage as ndi
import single_series_scrape as sss
import random
from skimage.segmentation import slic
from sklearn.cluster import KMeans, MeanShift, estimate_bandwidth, DBSCAN
from skimage.measure import regionprops
from sklearn.utils import shuffle
from matplotlib.colors import ListedColormap, rgb_to_hsv, hsv_to_rgb
from matplotlib import cm
from bin_color import bin_colors


def main():
    #  initial params for test
    testim_file = 'isotherm3.jpg'
    xaxes = [[97, 461], [583, 945]]
    yaxes = [[18, 340], [18, 340]]
    # testim_file = 'isotherm2.jpg'
    # xaxes = [[140, 932], [140, 888]]
    # yaxes = [[810, 1400], [50, 605]]

    #  read in image in color ans isolate the ROIs
    testim = io.imread(testim_file)
    # print type(testim)
    testim = testim.astype(np.float64)/255.0
    # testim = flt.gaussian(testim, 1, multichannel=True)
    # for i in range(testim.shape[2]):
    #     testim[..., i] = flt.median(testim[..., i], selem=np.ones((3, 3)))
    # testim = testim.astype(np.float64)/255.0
    # print testim.dtype
    # print testim.shape
    ROIs = [sss.isolate_ROI(testim, i, j, threshfxn=None) for i, j in
            zip(xaxes, yaxes)]

    plt.figure()
    ax1 = plt.subplot(1, 2, 1, adjustable='box-forced')
    ax2 = plt.subplot(1, 2, 2, adjustable='box-forced')
    ax1.imshow(ROIs[0])
    ax2.imshow(ROIs[1])
    ax1.set_title('First ROI, OG image')
    ax2.set_title('Second ROI, OG image')
    # plt.figure(2)
    # plt.imshow(ROIs[1])
    # plt.figure(3)
    # plt.imshow(testim)
    for ii, i in enumerate(ROIs):
        text = 'RGB colors, OG ROI number ' + str(ii)
        plot_colors(i, text)
        # im_recon, im_label = cluster_colorspace_ms(i)
        im_recon, im_label = cluster_colorspace_km(i, 4)
        plt.figure()
        ax1 = plt.subplot(121, adjustable='box-forced')
        ax2 = plt.subplot(122, adjustable='box-forced')
        ax1.imshow(im_recon)
        ax2.imshow(im_label, cmap='Set1')
        ax1.set_title('Reconstructed ROI number ' + str(ii))
        ax2.set_title('Labeled ROI number ' + str(ii))
        plot_colors(im_recon, title_text='RGB clusters, ROI num ' + str(ii))

    # im_km = cluster_colorspace_km(ROIs[0], 6)
    # plt.figure()
    # plt.imshow(im_km)
    # plot_colors(im_km)
    # label_im = slic(ROIs[0], n_segments=1024, compactness=1)
    # plt.figure()
    # plt.imshow(label_im, cmap='Set1')
    # bin_colors(ROIs[0], 4)
    plt.show()

    # my_cmap = convert_to_colormap(ROIs[0])


def plot_colors(im, title_text='RGB space'):
    """ For visualization purposes... im should have 3 color dimensions
    """
    xs, ys, zs = [im[:, :, i].reshape(-1) for i in range(im.shape[2])]
    bs = xs + ys + zs
    # thresh = flt.threshold_li(bs)
    thresh = 2.9
    bs = bs < thresh
    total = bs.sum()
    inds = range(total)
    inds = shuffle(inds, random_state=3)
    want = 5000
    xs = xs[bs][inds[0:want]]
    ys = ys[bs][inds[0:want]]
    zs = zs[bs][inds[0:want]]
    # print xs.shape
    # print inds[0:10]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(title_text)
    ax.scatter(xs, ys, zs)
    ax.set_ylim([0, 1])
    ax.set_xlim([0, 1])
    ax.set_zlim([0, 1])


def cluster_colorspace_km(im, n_clusters, train_size=5000):
    """ This function takes in an input image and a cluster number
        and clusters the image in RGB space using scikit's implementation
        of the kmeans shift algorithm.

        Args:
            im: w x h x 3 numpy array float64 with range [0,1] containing the
                image.
            n_clusters: number of clusters in color space to find
            train_size: number of points to use in training the model. default
                is 5000

        Returns:
            reconstructed im: w x h x 3 image where the inital rgb values have
                been replaced by the values of the cluster center that each
                point belongs to
            labeled im: w x h x 1 image where the value corresponds to the
                associated cluster label

    """
#    hsvimg = rgb_to_hsv(im)
    w, h, d = OG_shape = im.shape
    im_array = np.reshape(im,(w * h, d))
#    im_array = np.ravel(hsvimg[:,:,0]).reshape(-1,1) #, (w * h, d))

    print('KM: fitting model on a small sub-sample of the data')
    im_array_sample = shuffle(im_array, random_state=3)[:train_size]
    kmeans = KMeans(n_clusters=n_clusters, random_state=3).fit(im_array_sample)
    print('done fitting')

    print('KM: Prediciting color indiced on the full image')
    labels = kmeans.predict(im_array)
    print('done predicting')

    print('KM: recreating clustered image')
    im_comp = np.zeros((w, h, d))
    im_label = np.zeros((w, h))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            im_comp[i][j] = kmeans.cluster_centers_[labels[label_idx]]
            im_label[i][j] = labels[label_idx] + 1
            label_idx += 1
    im_label = np.squeeze(im_label.astype(int))
    return im_comp, im_label


def cluster_colorspace_ms(im, quant=0.1, train_size=5000, min_bin_freq=10):
    """ This function takes in an input image ans some optional parameters
        and clusters the image in RGB space using scikit's implementation
        of the mean shift algorithm.

        Args:
            im: w x h x 3 numpy array float64 with range [0,1] containing the
                image.
            quant: quantile used in determining distance between points. 0.5
                means that the median distance is used. default is 0.1
            train_size: number of points to use in training the model. default
                is 5000
            min_bin_freq: number of points in each initial bin for that bin to
                be considered a cluster center. default is 10

        Returns:
            reconstructed im: w x h x 3 image where the inital rgb values have
                been replaced by the values of the cluster center that each
                point belongs to
            labeled im: w x h x 1 image where the value corresponds to the
                associated cluster label

    """
    w, h, d = OG_shape = im.shape
    im_array = np.reshape(im, (w * h, d))

    print('MS: fitting model on a small sub-sample of the data')
    im_array_sample = shuffle(im_array, random_state=0)[:train_size]
    bw = estimate_bandwidth(im_array_sample, quantile=quant)

    print('MS: bandwidth estimated as: {0}'.format(bw))
    ms = MeanShift(bandwidth=bw, seeds=None, bin_seeding=True,
                   min_bin_freq=min_bin_freq, cluster_all=False)
    ms.fit(im_array_sample)
    print('MS: done fitting')

    print('MS: Prediciting color indiced on the full image')
    labels = ms.predict(im_array)
    unique_labels = np.unique(labels)
    print('done predicting')

    print('There are {0} labels'.format(sum(unique_labels > -1)))
    label_count = [sum(labels == i) for i in unique_labels]
    print('Labels and counts')
    for i, j in zip(unique_labels, label_count):
        print('For label {0}, there are {1} pts'.format(i, j))
    # print(ms.cluster_centers_)

    print('MS: recreating clustered image')
    im_comp = np.ones(im_array.shape)
    im_label = np.zeros((w * h))
    for ii, i in enumerate(range(w * h)):  # indices of the clustered pts
        im_comp[i, :] = ms.cluster_centers_[labels[ii]]
        im_label[i] = labels[ii] + 1
    im_comp.shape = OG_shape
    im_label.shape = (w, h)
    # labelfig = plt.figure()
    # labelfig.suptitle('Labeled image')
    # plt.imshow(im_label * 10, cmap='Set1')
    im_label = im_label.astype(int)
    return im_comp, im_label


def return_series(labeled_im):
    """
    """
    regions = regionprops(labeled_im)
    # attr = ['area', 'bbox', 'centroid', 'eccentricity', 'extent']
    # for i in regions:
    #     print('Label is: {0}'.format(i.label))
    #     for j in attr:
    #         print(j, i[j])
    exts = np.array([i.extent for i in regions])
    bknd = np.amax(exts)
    return [labeled_im == i.label for i in regions if i.extent != bknd]
if __name__ == '__main__':
    main()


# DONT USE THIS FUNCTION ON LARGE IMS DUE TO MEMORY SCALING.
# def cluster_colorspace_db(im):
#     """ Im should be a numpy array of float64 with range [0,1]
#     """
#     w, h, d = OG_shape = im.shape
#     im_array = np.reshape(im, (w * h, d))
#
#     print('DBSCAN: clustering a sub-sample of the data')
#     total_num = w * d
#     eps = (1.0/total_num)**(1.0/3.0)  # set min neighbor dist
#     min_pts = total_num/20.0  # aim for 20 or so clusters
#     db = DBSCAN(eps=eps, min_samples=min_pts)
#     db.fit(im_array)  # fit the nonsense
#     labels = db.labels_
#     clust_names = np.unique(labels)
#     print('DBSCAN: labels are:')
#     print(clust_names)
#
#     label_masks = [labels == i for i in clust_names]
#
#     print('DBSCAN: making a flat image')
#     im_comp = np.zeros((w, h))
#     label_idx = 0
#     for i in range(w):
#         for j in range(h):
#             im_comp[i][j] = labels[label_idx] + 2
#             label_idx += 1
#     return im_comp
