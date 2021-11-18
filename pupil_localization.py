def readImage(img):
    
    from skimage.io import imshow, imread
    from skimage.color import rgb2gray
    import numpy as np

    bmpImg = imread(img);
    greyScaleImg = rgb2gray(bmpImg);   # Y = 0.2125 R + 0.7154 G + 0.0721 B is used
    
    row=greyScaleImg.shape[0];
    col=greyScaleImg.shape[1];   

    return (greyScaleImg, bmpImg, (row,col));


'''
Reads raw eye image and converts to grey scale and calculates the dimensions

Parameters
----------
img
    RGB or bmp image


Returns
-------
greyScaleImg
    single value per pixel value range is 0-1
bmpImg 
    original image
(row, col)
    row and column size of the orginal image

'''



def binImg(greyScaleImg, threshold):
    
    from skimage.io import imshow, imread
    from skimage.color import rgb2gray
    import numpy as np

    row=greyScaleImg.shape[0];
    col=greyScaleImg.shape[1];

    rowCount=0;
    colCount=0;
    
    threshholdVal=threshold;

    binaryImgNormalized=np.zeros((row,col));
    binaryImg255=np.zeros((row,col));

    for rowVal in greyScaleImg:
        for pixel in rowVal:
            if pixel<threshholdVal:
                binaryImgNormalized[rowCount][colCount]=1;
                binaryImg255[rowCount][colCount]=255;
            colCount+=1;
        colCount=0;
        rowCount+=1;

    return (binaryImgNormalized, binaryImg255)


'''
Converts greyscale image to binary image

Parameters
----------
greyScaleImg
    grey scale image pixel value ranging from 0-1
threshold
    threshold value for the binary image
    
Returns
-------
binaryImgNormalized
    binary image with states: 0 and 1
binaryImg255
    binary image with states: 0 and 255. This is for graphical purposes since 0 and 1 does not plot well

'''




def turnToBlobs(binaryImage, diskRad):
    from skimage.morphology import erosion, dilation, disk

    footprint=disk(diskRad);

    dilatedArray = dilation(binaryImage, footprint);
    morphedArray=erosion(dilatedArray, footprint);
    
    return morphedArray


'''
Converts white pixel elements in binary elements into blobs for labelling

Parameters
----------
binaryImage
    binary image with state 0 to 1
diskRad
    the size in pixels of the radius of the morphing operation (dilation and then erosion)
    
Returns
-------
morphedArray
    image of the binary image with morphed elements with pixel value states either 0 to 1

'''




def returnPupilBlob(image):
    from skimage.morphology import label
    import numpy as np

    # returns a labelled array where saem blob is given same number
    labelledArray = label(image,return_num=True)
    
    # iterate through labelledArray and find the biggext blob area
    # array shape: row x col 240 x 320

    # iterate through the array and increment for each unique array value
    blobSizeArray = np.zeros(labelledArray[1]+1);  # plus one because there are index+1 number of indexes (e.g. last index number:10 then number of indexes:11)
    for row in labelledArray[0]:
        for pixel in row:
            if pixel != 0:
                # search pixel value in blobSizeArray and increment blobSizeArray
                # blobSizeArray index corresponds to labelledArray pixel value
                blobSizeArray[pixel] += 1;

    largestArea=0;
    count=0;
    index=0;
    for area in blobSizeArray:
        if area>largestArea:
            largestArea=area;
            index=count;
        count+=1;
        
        
    # turn array value with pupil index to 1 and everything else 0
    rowCount=0;
    colCount=0;
    #count=0;

    # create zeros array of the image
    # fix the arugment with universal variable name (static name)
    finalBinArray=np.zeros([labelledArray[0].shape[0], labelledArray[0].shape[1]]);

    for row in labelledArray[0]:
        for pixel in row:
            if pixel==index:
                finalBinArray[rowCount][colCount]=1;
            colCount+=1;
        colCount=0;
        rowCount+=1;
    
    return finalBinArray



'''
Returns the binary image with only the pupil element

Parameters
----------
image
    morphed image from the turnToBlobs()

Returns
-------
finalBinArray
    binary image with only the pupil element pixel value range 0-1
'''



def pupilCircle(pupilBlob, sig=3, low_thresh=0, high_thresh=1, radiusRangeStart=1, radiusRangeEnd=70):

    from skimage.feature import canny
    import numpy as np
    from skimage.transform import hough_circle
    
    
    edgeImg=canny(pupilBlob, sigma=sig, low_threshold=low_thresh, high_threshold=high_thresh)

    # radius range
    try_radii = np.arange(radiusRangeStart, radiusRangeEnd)
    accumulatorMatrix = hough_circle(edgeImg, try_radii)  # returns a 3D accumulatorMatrix: a (240) x b (320) x radius range (45)

    # find the index number with the highest accumulator value
    index=np.argmax(accumulatorMatrix);
    # find the coordiante values for the above index
    # the coordinates are: radius, r (row of center), c (column of center)

    radius, r, c = np.unravel_index(index, accumulatorMatrix.shape);

    
    return (radius,r,c)



'''
Returns the circle parameters of the pupil: radius and center coordinates

Parameters
----------
pupilBlob
    binary image with pupil element only pixel values 0-1
sig : default = 3
    canny edge detection sigma value is higher for less sensitive edge detection
low_thresh : default = 0
    pixel value in low pixel value range in image (0)
high_thresh : default = 1
    pixel value in high pixel value range in image (1)
radiusRangeStart : default = 0
    start radius value for Hough transform
radiusRangeEnd : default = 70
    end radius value for Hough transform


Returns
-------
(radius, r, c)
    tuple with the radius, row and column of the pupil circle
'''


