# This is a demo for iris code and matching
# The aim is to generate a 50 bit iris code and a 50 bit bitmask


from Iris_code_and_matching import *

def iris_code_and_bitmask(normalizedIrisImg):
    #create ternary image
    ternImg = ternaryImg(normalizedIrisImg);
    # gernerate iris code and bitmask type tuple
    irisCode_Bitmask = generateIrisCode(ternImg);
    
    return irisCode_Bitmask


'''
it takes in the output from the iris-segmentation stage and outputs a tuple of iris code and bitmask

Parameters
----------
normalizedIrisImg
	image from iris_segmentation stage

Returns
-------
irisCode_Bitmask
	a tuple with 50 bit iris code and 50 bit bitmask


'''