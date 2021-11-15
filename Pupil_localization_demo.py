# This is a demo for pupil localization
# This is the first step inpre-processing
# The aim is to find the circle parameters of the pupil center

from pupil_localization import *

# read image
eyeImage = readImage("aeval1.bmp");
greyscaleImg = eyeImage[0];
# binary image with threshold value of 0.2
binaryImg = binImg(greyscaleImg, 0.2)[0];
# morphological operator value set to 3px. this is the disk size
labelledImg = turnToBlobs(binaryImg, 3);
pupilBlobImg = returnPupilBlob(labelledImg);
circleParam = pupilCircle(pupilBlobImg);

print(circleParam)