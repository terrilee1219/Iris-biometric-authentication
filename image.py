# read image
# write functions

def image(img, threshVal):   
    
    from skimage.io import imshow, imread
    from skimage.color import rgb2gray
    import numpy as np

    bmpImg = imread(img);
    greyScaleImg = rgb2gray(bmpImg);   # Y = 0.2125 R + 0.7154 G + 0.0721 B is used
    #print(img)
    row=greyScaleImg.shape[0];
    col=greyScaleImg.shape[1];
    
    
    # create binary image
    # create zero array with correct shape
    rowCount=0;
    colCount=0;

    threshholdVal=threshVal;

    binaryImg=np.zeros((row,col));

    for rowVal in greyScaleImg:
        for pixel in rowVal:
            if pixel<threshholdVal:
                binaryImg[rowCount][colCount]=1;
            colCount+=1;
        colCount=0;
        rowCount+=1;
    #print(binaryImg) 
    
    
    

    return (greyScaleImg, binaryImg, bmpImg, (row,col));

    
'''
function: img(img, threshVal)

parameters
img: bmp image file
threshVal: threhold value betwee 0 and 1 for binary image creation

Returns
output: (grey scale image array, binary image, original bmp image array, (row, col))
grey scale image array is: (0.2125 R + 0.7154 G + 0.0721 B)/255 a percentage of 255
(row, col) is a tuple of the size of image array
'''
