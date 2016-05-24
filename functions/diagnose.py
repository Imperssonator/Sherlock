import numpy as np
import os
import skimage.io as io
import skimage.color as color
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.ndimage as ndi
import single_series_scrape as sss
from matplotlib import cm
from bin_color import find_dom_color
import cluster_data as cld
import skimage.morphology as mph


testim_file = '../examples/isotherm3.jpg'
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
st = np.ones((3, 3))  # 2D connectivity structure element

for ii, i in enumerate(ROIs):
    if ii == 1:
        cld.plot_colors(i, title_text='RGB space, ROI {0}'.format(ii),
                        tform=None)
        cld.plot_colors(i, title_text='LAB space, ROI {0}'.format(ii),
                        tform=color.rgb2lab)
        cld.plot_colors(i, title_text='XYZ space, ROI {0}'.format(ii),
                        tform=color.rgb2xyz)
        bknd_mask = find_dom_color(i, pltcolor=False)
        plt.figure()
        plt.imshow(bknd_mask, cmap='viridis')
        plt.suptitle('no erosion')
        bknd_mask = mph.dilation(bknd_mask, selem=st)
        plt.figure()
        plt.imshow(bknd_mask, cmap='viridis')
        plt.suptitle('one dilation')


plt.show()
