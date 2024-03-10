import numpy as np
import cv2

def CreateDetector():
    #setup Aruco Detector and which marker library see https://chev.me/arucogen/
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50) # we will use marker 0 of the dictionary, 50 cm^2 as of rn
    arucoParams = cv2.aruco.DetectorParameters() # use default detect params
    detector = cv2.aruco.ArucoDetector(arucoDict,arucoParams) #define detector object
    return(arucoDict,arucoParams,detector)

