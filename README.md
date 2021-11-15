Language used: Python version 3.0

All the functions have the function descriptions

The system is divided into 3 stages:

1.) Pupil localization
2.) Iris segmentation
3.) Iris code and matching

The first step is pupil localization. (Refer to research for more detail)
1.) Pupil localization has 5 functions

- readImage()
- binImg()
- turnToBlobs()
- returnPupilBlobs()
- pupilCircle()

An bmp or RGB eye image enters this stage and the pupil parameters are outputted: radius, center coordinates. The Pupil_localization_demo script shows how to use the functions.


The next step is iris segmentation:
2.) Iris segmentation has 7 functions

- cannyEdge()
- sweepingLine()
- sweepIris()
- pupilIrisCircle()
- contourCrop()
- irisRectangle()
- normalizeIrisImg()

The output from this stage is a normalized (resized, noise removed) rectangular iris image. Iris_segmentation_demo shows how to use the functions.


3.) Iris code and matching has 4 functions

- ternaryImg()
- generateIrisCode()
- match()


more detailed instructions on how to use the functions to come soon