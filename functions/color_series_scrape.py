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


def main():
    testim_file = 'isotherm3.jpg'
    xaxes = [[97, 461], [583, 945]]
    yaxes = [[18, 340], [18, 340]]
    pts = color_series_scrape(testim_file, xaxes, yaxes, n_colors=4)
    for ROI, _ in enumerate(xaxes):
        data = pts[ROI]
        print('ROI number {0}'.format(ROI))
        for ss, series in enumerate(data):
            print('... Series number {0}'.format(ss))
            for pt in series:
                print('... ... {0}'.format(pt))


def color_series_scrape(rgb_im, xaxis, yaxis, n_colors=None):
    im_raw = io.imread(rgb_im)
    im_raw = im_raw.astype('float64')/255.0
    ROIs = [sss.isolate_ROI(im_raw, i, j, threshfxn=None) for i, j in
            zip(xaxis, yaxis)]
    pts = []
    for i in ROIs:
        if n_colors is not None:
            im_recon, im_label = \
                cld.cluster_colorspace_km(i, n_clusters=n_colors)
        else:
            im_recon, im_label = cld.cluster_colorspace_ms(i)
        labels_as_ims = cld.return_series(im_label)
        pts.append([sss.isolate_Points(j) for j in labels_as_ims])
    return pts, ROIs


if __name__ == '__main__':
    main()
