import numpy as np
import os
import skimage.io as io
import matplotlib.pyplot as plt
import skimage.filters as flt
import skimage.morphology as mph
import scipy.ndimage as ndi

""" This file contains the functions needed to scrape a single series off of a
    plot.

    Created by @perrywmellis on 10 April 2016
    pellis30@gatech.edu

"""


def isolate_ROI(im, xaxis, yaxis, threshfxn=flt.threshold_li):
    """ This function returns the binarized ROI in "im" defined by the "xaxis"
        and "yaxis"

        Args:
            im: ND numpy array
            xaxis: [start col, end col] .. 2 element list defining the position
                   and length of the x axis of ROI
            yaxis: [start row, end row] .. 2 element list defining the position
                   and length of the y axis of the ROI
            threshfxn: function to threshold the ROI. Default is the skimage
                       implementation of li's threshold. If threshfxn == None,
                       returned image is NOT binary

        Returns:
            ND numpy array size (end row- start row, end col - start col, ...)
            encompassing the ROI binarized such that 0 is background and 1 is
            foreground
    """

    ROI = im[yaxis[0]:yaxis[1], xaxis[0]:xaxis[1], ...]
    if threshfxn is not None:
        out = ROI < threshfxn(ROI)

        # check to make sure background is 0
        if out.sum() > float(out.size)/2.0:
            out = ~out
    else:
        out = ROI

    return out


def try_thresh(im, filter, fig_num):
    """ Helper function to try different threshold routines

        Args:
            im: image to threshold
            filter: thresholding filter to use. Must return a scalar
            fig_num: figure number to plot the output

        Returns:
            Nothing

    """
    thresh = filter(im)
    binary = im > thresh

    plt.figure(fig_num)
    ax1 = plt.subplot(1, 3, 1, adjustable='box-forced')
    ax2 = plt.subplot(1, 3, 2)
    ax3 = plt.subplot(1, 3, 3, adjustable='box-forced')

    ax1.imshow(im)
    ax1.set_title('OG IM')
    ax1.axis('off')

    ax2.hist(im.ravel())
    ax2.set_title('Histogram')
    ax2.axvline(thresh, color='r')

    ax3.imshow(binary, cmap=plt.cm.gray)
    ax3.set_title('Thresholded')
    ax3.axis('off')


def isolate_Points(binary_im, open_markers=False, return_im=False):
    """ This function takes in a binary image with a single series of data that
        are points connected by lines. The function then finds the location
        of the points and returns their [row, col] positions as a list

        Args:
            binary_im: binary image containing the data. The data (foreground)
                       should be 1's and the background should be 0's.
            open_markers: logical flag that is False for filled markers and
                          True for open markers. Default is False.
            return_im: logical flag. Set to True to return the labeled image.
                       Default is False

        Returns:
            N x 2 list where N is the number of points and each row has the
            [row, col] position of the point.

            labeled image where each labeled area corresponds to a marker

    """
    if open_markers is False:
        im = temp = binary_im
    else:
        im = temp = mph.remove_small_holes(binary_im, connectivity=2)

    st = np.ones((3, 3))  # 2D connectivity structure element
    count = 0
    while temp.sum() > 0:
        count += 1
        temp = mph.binary_erosion(temp, selem=st)

    #  erode 2 iterations away from everything to isolate data markers
    while count - 2 > 0:
        count -= 1
        im = mph.binary_erosion(im, selem=st)

    # label the marker regions and calculate the center of mass of each region
    temp, nlabels = mph.label(im, background=0, return_num=True,
                              connectivity=2)
    CoM = ndi.measurements.center_of_mass(im, temp, range(nlabels+1)[1:])

    if return_im is False:
        return CoM
    else:
        return CoM, temp


if __name__ == '__main__':
    #  initial params for test
    testim_file = 'isotherm1.png'
    xaxis = [130, 584]  # in px
    yaxis = [63, 447]  # in px

    #  read in image as grey (flag 0)
    testim = io.imread(testim_file, as_grey=True)

    #  isolate the ROI and plot it
    testROI = isolate_ROI(testim, xaxis, yaxis)
    plt.figure(11)
    plt.imshow(testROI)

    #  find the markers and return their locations and the labeled image
    locs, labeled = isolate_Points(testROI, open_markers=False, return_im=True)
    plt.figure(1)
    plt.imshow(labeled)
    print(locs)

    plt.show()
