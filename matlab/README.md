# MATLAB Spatial Stats

## Driver_Imscrape

Run this to perform spatial stats/PCA on all of the images in scrape_figures\dump... you may have to change "FolderName"

Automatically loads all the data that was generated during the process.

"Files" is a struct with info on the images

## disp_img

usage: disp_img(i,Files)

* display the image with index "i" from the struct "Files", which is automatically loaded after running Driver_Imscrape

## SS_Dir

The function that runs a directory of images through SS_PCA

## bradley

A very good thresholding procedure that uses the image integral somehow.
