# This is a demo for iris segmentation
# This is the second step in pre-processing
# The aim is to get a normalized (resized, noise removed), rectangular, greyscale (pixel value range 0-1) iris image

from iris_segmentation import *
from pupil_localization import *
import matplotlib.pyplot as plt

def irisRectImage(pupilTuple, image, resolution=(490,50)):

    # read eye image
    eyeImg = readImage(image);
    # convert to greyscale for canny
    greyscaleImg = eyeImg[0];
    # convert to edge image
    cannyImg = cannyEdge(greyscaleImg);
    # find iris border radius
    irisBorderRadius = sweepIris(cannyImg, pupilTuple, startAngle=0, endAngle=45)[4];
    # iris parameter tuple is the same as the pupil tuple except for the radius value
    irisTuple = (irisBorderRadius, pupilTuple[1], pupilTuple[2]);
    # plot pupil and iris border on top of original image for illustration
    plt.imshow(pupilIrisCircle(image, pupilTuple, irisBorderRadius)[3]);
    # iris rectangualr image
    irisRectImage = irisRectangle(greyscaleImg, irisTuple, pupilTuple);
    # normalize iris image
    # resolution can be set to any value
    irisImgNormalized = normalizeIrisImg(irisRectImage, resolution);

    return irisImgNormalized


'''
Takes in raw eye image and the pupil parameters from the pupil localization stage (radius, center row, center col) and outputs normalized (resized, noise removed), rectangular, greyscale (pixel value range 0-1) iris image

Parameters
----------
pupilTuple
    tuple value of pupil
image
    original eye image
resolution
    tuple (row, col) of desired fixed iris image resolution
    
Returns
-------
irisImgNormalized
    greyscale (value range 0-1) of certain resolution, rectangular iris image wiht noise set to pixel value 0
'''












