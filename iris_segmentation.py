def cannyEdge(greyImg, sig=2):
    from skimage.feature import canny
    edgeImg=canny(greyImg, sigma=sig)  # report: explain canny and show edge detection for different values og sigma
    
    return edgeImg;


'''
Converts grey scale eye image into edge image

Parameters
----------
greyImg
    grey scale image of eye image pixel value range 0-1
sig : default = 2
    sigma value for edge detection. Higher the value, lower the sensitivity of edge detection
    
Returns
-------
edgeImg
    a binary edge image of the eye
'''



def sweepingLine(tupleVal,angle, multiple=3):
    import numpy as np
    import math
    
    # create a python list: for unknown length and convert it to numpy for numpy operations
    # will store the sweeping line pixels
    sweepingLine=[];
    radius=tupleVal[0];
    rowCenter=tupleVal[1];
    colCenter=tupleVal[2];

    # step1: how many columns for the given radius and angle (col is what i will iterate by 1)
    # initially: the radius of the pupil times 2.5
    maxCol=3*radius*math.cos(2*math.pi*(angle/360));  # in radians
    # round up
    maxCol = math.ceil(maxCol);
    
    
    for i in range(1,maxCol,1):
        #work out the rounded down row val for col from 1-maxCol
        rowVal=math.tan(2*math.pi*(angle/360))*i;
        rowVal=math.floor(rowVal);  # round down
        
        sweepingLine.append([rowCenter+rowVal,colCenter+i+1]);  # plus 1 because it is pixel to the right of current one

        # step 2: do same for row
    maxRow=multiple*radius*math.sin(2*math.pi*(angle/360));  # in radians
    # round up
    maxRow = math.ceil(maxRow);
    
    for i in range(1, maxRow, 1):
        colVal=math.tan(2*math.pi*((90-angle)/360))*i;   # 90-angle
        colVal=math.floor(colVal);
        
        sweepingLine.append([rowCenter+i,colCenter+colVal+1]);  # look at diagram, we need to add 1 due to placement of origin

    # sort the sweepingLine pixels in ascending order for easier use
    def myFunc(e):
        return e[0]
    
    sweepingLine.sort(key=myFunc);  

    return sweepingLine


'''
Creates a straight line of length multiple multiplied by pupil radius from center of pupil at given angle 

Parameters
----------
tupleVal
    (radius, rowCenter, colCenter) of the pupil center
angle
    angle in degrees. 0 degrees at the positive x axis and positive angles in clockwise direction
multiple
    constant multiplied by the pupil radius for sweeping line. This value must be larger than the iris border

Returns
-------
swepingLine
    2D array of [row, col] all pixels in the sweepingline
'''




def sweepIris(cannyImg, tupleVal, startAngle=0, endAngle=45):
    
    import numpy as np
    import copy
    import math
    
    image=np.array(cannyImg);
    sweep=[];
    intersectArray=[];
    irisRadiusArray=[];   #keeps radius of border crossings
    
    
    for angle in range(startAngle, endAngle, 1):
        #print(angle)
        sweep=sweepingLine(tupleVal, angle);
        
        # code version 2
        for pixel in sweep:
            if image[pixel[0]][pixel[1]]==1:
                intersectArray.append(pixel);
            
            
    # iris border
    # radius threshold: pupil radius*1.2
    irisIntersectArray=copy.deepcopy(intersectArray);    # make deep copy to leave original array of pupil and iris intact
    threshold=tupleVal[0];
    for pixel in intersectArray:
        radius=math.sqrt((pixel[0]-tupleVal[1])**2 + (pixel[1]-tupleVal[2])**2);
        #radiusArray.append(radius);
        #print(radius);
        # remove any pixel where radius<pupil radius*1.2
        if radius < 1.2*tupleVal[0]:
            irisIntersectArray.remove(pixel);
            #print("removed")
        else:
            irisRadiusArray.append(radius);

        
    # return iris border radius average
    radiusSum=0;
    radiusAverage=0;
    for radius in irisRadiusArray:
        radiusSum+=radius;
    try:
        radiusAverage=round(radiusSum/len(irisRadiusArray));
    except(ZeroDivisionError):
        radiusAverage="no intersections"
        pass

            
    return (image,intersectArray,irisIntersectArray,radiusArray,radiusAverage)



'''
sweeps an edge image with a sweeping line and records edge intersections over angle range

Parameters
----------
cannyImg
    edge image of eye
tupleVal
    (radius, row, column) of the pupil
startAngle
    angle to start the sweep (0 at positive x axis and positive in clockwise direction)
endAngle
    angle to end the sweep (0 at positive x axis and positive in clockwise direction)
    
Returns
-------
image
    numpy array version of canny iamge
intersectArray
    an array of all intersection pixels between the edge image and the sweeping line for the angle range
irisIntersectArray
    an array of intersection pixels between iris border and the sweeping line (this is done by removing any intersections below 1.2 times pupil radius)
irisRadiusArray
    radius of all intersections with 1.2 times pupil radius removed
radiusAverage
    average radius value of the irisRadiusArray values
'''




def pupilIrisCircle(RGBImage,tupleVal,irisRadius):
    
    # create binary image of iris circle contour
    from skimage.draw import circle_perimeter  # library for drawing circle perimeter
    import copy
    import numpy as np
    from pupil_localization import readImage
    
    imageRead = imageRead(RGBImage);
    
    rows=imageRead[2][0];
    cols=imageRead[2][1];
    copyRGB=copy.deepcopy(RGBImage);

    # initialize the empty arrays
    binImageIrisPupil = np.zeros((rows,cols), dtype=bool);
    binImageIris=np.zeros((rows,cols), dtype=bool);
    binImagePupil=np.zeros((rows,cols), dtype=bool);
    
    rri, cci = circle_perimeter(tupleVal[1],tupleVal[2],irisRadius);
    binImageIris[rri, cci] = 1;
    copyRGB[rri, cci]=[0,255,0];  # green

    rrp, ccp = circle_perimeter(tupleVal[1],tupleVal[2],tupleVal[0]);
    binImagePupil[rrp, ccp] = 1;
    copyRGB[rrp, ccp]=[0,255,0];  # green
    binImageIrisPupil=np.add(binImageIris, binImagePupil);

    return (binImageIrisPupil, binImagePupil, binImageIris, copyRGB)


'''
For plotting the iris circle and the pupil circle for illustration purposes

Parameters
----------
RGBImage
    original eye image
tupleVal
    (radius,row,col) of the pupil
irisRadius
    iris radius

Returns
-------
binImageIrisPupil
    binary array with iris and pupil border
binImagePupil
    binary image with pupil border
binImageIris
    binary image with iris border
copyRGB
    original RGB image with the pupil and iris border overlay in green: (0,255,0)
'''



def contourCrop(greyScaleImage, tupleVal):
   
    import copy
    import numpy as np
    
    #print(greyScaleImage.shape)

    radius=tupleVal[0];
    rowCenter=tupleVal[1];
    colCenter=tupleVal[2];
    copyImg=copy.deepcopy(greyScaleImage);


    from skimage.morphology import disk

    # use disk function
    # the disk function returns a square matrix of size radius*2+1 x radius*2+1 
    circle=disk(radius);
    #print(circle);
    circleCropped=np.zeros((radius*2+1,radius*2+1));
    rowCount=0;
    colCount=0;
    for row in circle:
        for pixel in row:
            if pixel:
                # disk origin: (radius,radius)
                circleCropped[rowCount][colCount]=greyScaleImage[(rowCenter-radius)+rowCount][(colCenter-radius)+colCount];
                #print(str(rowCount)+":"+str(colCount)+str(a))
                copyImg[(rowCenter-radius)+rowCount][(colCenter-radius)+colCount]=0;
            colCount+=1;
            #print("row: "+str(rowCount)+" col: "+str(colCount));
        colCount=0;
        rowCount+=1;
        
    return (circleCropped,copyImg)


'''
Circular crop of image

Parameters
----------
greyScaleImage
    greyScale eye image
tupleVal
    (radius, row, column) of circle to crop
    
Returns
-------
circleCropped
    circle image extracted out (square image of size: radius+1 by radius+1)
copyImg
    original grey scale image without the circleCropped

'''




def irisRectangle(greyScaleImg, tupleValIris, tupleValPupil, noiseSigma=2, diskSize=10):
    
    from iris_segmentation import contourCrop
    
    import polarTransform
    import numpy as np
    import matplotlib.pyplot as plt
    
    from skimage.feature import canny
    import copy
    from skimage.morphology import erosion, dilation, disk
    #from skimage.io import imshow

    pupilAndIris=contourCrop(greyScaleImg,tupleValIris)[0];
    # pupil center is the center of the new square image: row x col = irisradius x irisradius
    pupilParam = list(tupleValPupil);
    pupilParam[1] = tupleValIris[0]; # row of pupil center is iris radius
    pupilParam[2] = tupleValIris[0]; # col of pupil center is iris radius
    pupilParam = tuple(pupilParam);
    iris=contourCrop(pupilAndIris,pupilParam)[1];
    #imshow(iris)
    


    polarImage, ptSettings = polarTransform.convertToPolarImage(iris, initialRadius=tupleValPupilAdj[0],finalRadius=tupleValIris[0], initialAngle=0,finalAngle=2 * np.pi);


    copyImg=copy.deepcopy(polarImage);
    # it is a binary image
    edgeImg=canny(copyImg,sigma=noiseSigma);

    # apply morphological operators to images
    footprint=disk(diskSize);

    dilatedArray = dilation(edgeImg, footprint);
    morphedArray=erosion(dilatedArray, footprint);

    #remove
    colCount=0;
    rowCount=0;

    irisImg=copy.deepcopy(polarImage);

    for row in morphedArray:
        for pixel in row:
            if pixel:
                irisImg[rowCount][colCount]=0;
            colCount+=1;
        colCount=0;
        rowCount+=1;

    #imshow(irisImg);
    
    return irisImg


'''
Turn iris image to rectangular image with noise features set to 0

Parameters
----------
greyScaleImg
    grey scale image of the iris image
tupleValIris
    (radius, row, column) of iris
tupleValPupil
    (radius, row, column) of pupil
noiseSigma : default = 2
    sigma value for edge detection of noise element
diskSize : default = 10
    disk radius for morphological operation for noise element blob creation

Return
------
irisImg
    unwrapped image of iris (rectangular) with noise elements set to pixel value 0

'''


    

def normalizeIrisImg(irisRectImg, resolution):
    from pupil_localization import readImage
    from skimage.transform import resize
    from skimage.exposure import histogram
    import matplotlib.pyplot as plt
    from skimage import exposure
    import numpy as np
    
    # step 1: greyscale
    images=readImage(irisRectImg);
    greyImage=images[0];
    
    #step 2: resize
    resizedImage = resize(greyImage,resolution)

    # histogram equlization
    equalizedImage = exposure.equalize_hist(resizedImage);

    return equalizedImage

'''
normalize rectangular iris image: resize, equalize image

Parameters
----------
irisRectImg
    rectangular iris image from the irisRectangle()
resolution
    resolution of the desired output image in pixels: row by col

Returns
-------
equalizedImage
    grey scale image with value 0-1 that is resized and histogram equalized

'''



