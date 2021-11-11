def readImage(img):
    
    from skimage.io import imshow, imread
    from skimage.color import rgb2gray
    import numpy as np

    bmpImg = imread(img);
    greyScaleImg = rgb2gray(bmpImg);   # Y = 0.2125 R + 0.7154 G + 0.0721 B is used
    
    row=greyScaleImg.shape[0];
    col=greyScaleImg.shape[1];   

    return (greyScaleImg, bmpImg, (row,col));




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







def turnToBlobs(binaryImage, diskRad):
    from skimage.morphology import erosion, dilation, disk

    footprint=disk(diskRad);

    dilatedArray = dilation(binaryImage, footprint);
    morphedArray=erosion(dilatedArray, footprint);
    
    return morphedArray







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







def pupilCircle(pupilBlob):

    from skimage.feature import canny
    import numpy as np
    edgeImg=canny(pupilBlob, sigma=3, low_threshold=0, high_threshold=1)
    
    # hough transform the edge image

    from skimage.transform import hough_circle
    # radius range
    try_radii = np.arange(1, 70)
    accumulatorMatrix = hough_circle(edgeImg, try_radii)  # returns a 3D accumulatorMatrix: a (240) x b (320) x radius range (45)

    # find the index number with the highest accumulator value
    index=np.argmax(accumulatorMatrix);
    # find the coordiante values for the above index
    # the coordinates are: radius, r (row of center), c (column of center)

    radius, r, c = np.unravel_index(index, accumulatorMatrix.shape);

    #print("The radius is: " + str(radius));
    #print("The row val for center of circle: "+str(r));
    #print("The col val for center of circle: "+str(c));
    
    return (radius,r,c)






