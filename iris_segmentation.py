def cannyEdge(greyImg):
    from skimage.feature import canny
    edgeImg=canny(greyImg, sigma=2)  # report: explain canny and show edge detection for different values og sigma
    
    return edgeImg;


'''
function: cannyEdge(greyImg)

parameter
binImg: a binary image of value 0 or 1

returns


'''



def sweepingLine(tupleVal,angle):
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
    maxRow=3*radius*math.sin(2*math.pi*(angle/360));  # in radians
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
function sweepingLine(tupleVal,angle)

parameter:
tupleVal: (radius, rowCenter, colCenter) of the pupil center
angle: angle of the sweeping line to be generated

returns: array of dimension nx2 where n is the number of pixels in the sweepingline and 2 is rowxcol of sweeping line pixel
'''





def sweepIris(cannyImg, tupleVal):
    
    import numpy as np
    import copy
    import math
    
    image=np.array(cannyImg);
    sweep=[];
    intersectArray=[];
    radiusArray=[];   #keeps radius of border crossings
    
    
    # 0 degrees to -45 degrees
    for angle in range(45):
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
            radiusArray.append(radius);

        
    # return iris border radius average
    radiusSum=0;
    radiusAverage=0;
    for radius in radiusArray:
        radiusSum+=radius;
    try:
        radiusAverage=round(radiusSum/len(radiusArray));
    except(ZeroDivisionError):
        radiusAverage="no intersections"
        pass

            
    return (image,intersectArray,irisIntersectArray,radiusArray,radiusAverage)



def pupilIrisCircle(RGBImage,tupleVal,irisRadius):
    
    # create binary image of iris circle contour
    from skimage.draw import circle_perimeter  # library for drawing circle perimeter
    import copy
    import numpy as np
    
    rows=240;
    cols=320;
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
function pupilIrisCircle()

Input parameters
RGBImage: bmp image in the database. It acts like RGB image
tupleVal: (radius,row,col) of the pupil
irisRadius: iris radius

Returns
binImageIrisPupil: binary array with shape==image shape and iris pupil border is set to 1
binImagePupil: pupil border
binImageIris: iris border
copyRGB: the original bmp image with the pupil iris border overlay in green: (0,255,0)

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




def irisRectangle(greyScaleImg, tupleValIris, tupleValPupilAdj):
    
    from iris_segmentation import contourCrop
    
    import polarTransform
    import numpy as np
    import matplotlib.pyplot as plt
    
    from skimage.feature import canny
    import copy
    from skimage.morphology import erosion, dilation, disk
    #from skimage.io import imshow

    pupilAndIris=contourCrop(greyScaleImg,tupleValIris)[0];
    iris=contourCrop(pupilAndIris,tupleValPupilAdj)[1];
    #imshow(iris)
    


    polarImage, ptSettings = polarTransform.convertToPolarImage(iris, initialRadius=tupleValPupilAdj[0],finalRadius=tupleValIris[0], initialAngle=0,finalAngle=2 * np.pi);
    # canny


    copyImg=copy.deepcopy(polarImage);
    # it is a binary image
    edgeImg=canny(copyImg,sigma=2);

    # apply morphological operators to images
    footprint=disk(10);

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
    

def normalizeIrisImg(irisRectImg, resolution, thresholdVal):
    from pupil_localization import readImage, binImg
    from skimage.transform import resize
    from skimage.exposure import histogram
    import matplotlib.pyplot as plt
    from skimage import exposure
    import numpy as np
    
    # step 1: greyscale
    images=readImage(irisRectImg);
    greyImage=images[0];
    binImage=binImg(greyImage)[0];
    
    ternImage=np.empty([resolution[0],resolution[1]]);
    originalResolution=images[2];
    
    #step 2: resize
    resizedImage = resize(greyImage,resolution)

    # histogram equlization
    equalizedImage = exposure.equalize_hist(resizedImage);

    return equalizedImage




