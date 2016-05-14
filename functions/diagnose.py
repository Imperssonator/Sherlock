import numpy as np
import os
import skimage.io as io
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.ndimage as ndi
import single_series_scrape as sss
from matplotlib import cm
from bin_color import bin_colors
import cluster_data as cld

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

for ii, i in enumerate(ROIs):
    im_recon, im_label = cld.cluster_colorspace_km(i, 4)
    print('ROI number {0}'.format(ii))
    labels_as_ims = cld.return_series(im_label)
    for jj, j in enumerate(labels_as_ims):
        plt.figure()
        plt.imshow(j, cmap='viridis')
        plt.suptitle('Region {0} Label {1}'.format(ii, jj))
        print("COMs for Region {0} and Label {1}".format(ii, jj))
        pts = sss.isolate_Points(j)
        print(len(pts), pts)
    pts = [sss.isolate_Points(j) for j in labels_as_ims]
    plt.figure()
    plt.imshow(im_recon)
    plt.hold(True)
    markers = ['o', 'v', '^', '<', '>']
    for ii, series in enumerate(pts):
        xs = [k[1] for k in series]
        ys = [k[0] for k in series]
        plt.scatter(xs, ys, c='g', marker=markers[ii])
    plt.hold(False)
plt.show()
