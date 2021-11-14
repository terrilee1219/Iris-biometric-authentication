Python version 3.0

The system is divided into 3 stages:

1.) Pupil localization
2.) Iris segmentation
3.) Iris code and matching


1.) Pupil localization has 5 functions

- readImage()
- binImg()
- turnToBlobs()
- returnPupilBlobs()
- pupilCircle()


2.) Iris segmentation has 7 functions

- cannyEdge()
- sweepingLine()
- sweepIris()
- pupilIrisCircle()
- contourCrop()
- irisRectangle()
- normalizeIrisImg()

3.) Iris code and matching has 4 functions

- ternaryImg()
- generateIrisCode()
- match()


more detailed instructions on how to use the functions to come soon