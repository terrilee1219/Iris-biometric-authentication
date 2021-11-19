Language used: Python version 3.0


The iris biometric authentication system is divided into 3 stages:

- Pupil localization
- Iris segmentation
- Iris code and matching

Each stages are written as seperate libraries:
- pupil_localization
- iris_segmentation
- iris_code_and_matching

Each stage has an accompanying demo script with a single function call that executes all the functions in each of the libraries. The demo scripts should be run in the order of the stages laid out above and are named:
- Pupil_localization_demo.py
- Iris_segmentation_demo.py
- Iris_code_and_matching_demo.py

A demo image is uploaded for use for the demo. They are named:
- aeval1.bmp
- chingycr1.bmp
- kelvinr1.bmp

The first step is pupil localization
Pupil localization has 5 functions

- readImage()
- binImg()
- turnToBlobs()
- returnPupilBlobs()
- pupilCircle()

An bmp or RGB eye image enters this stage and the pupil parameters are outputted: radius, center coordinates. The Pupil_localization_demo script shows how to use the functions.


The next step is iris segmentation:
Iris segmentation has 7 functions

- cannyEdge()
- sweepingLine()
- sweepIris()
- pupilIrisCircle()
- contourCrop()
- irisRectangle()
- normalizeIrisImg()

The output from this stage is a normalized (resized, noise removed) rectangular iris image. Iris_segmentation_demo shows how to use the functions.

The next step is iris code generation and matching.
Iris code and matching has 4 functions

- ternaryImg()
- generateIrisCode()
- match()


more detailed instructions on how to use the functions to come soon