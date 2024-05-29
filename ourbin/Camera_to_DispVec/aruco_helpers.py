import numpy as np
import cv2
import math

def CreateDetector():
    # set up Aruco Detector and which marker library see https://chev.me/arucogen/
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50) # we will use marker 0 of the dictionary, 50 cm^2 as of rn
    arucoParams = cv2.aruco.DetectorParameters() # use default detect params
    detector = cv2.aruco.ArucoDetector(arucoDict,arucoParams) #define detector object
    return(arucoDict,arucoParams,detector)

def GetRelativeYaw(corners): # calcs only for the corners of 1st aruco, i.e. with lowest id # in set
    x1= int(corners[0][0][0][0])
    y2= int(corners[0][0][0][1])
    x2= int(corners[0][0][1][0])
    y1= int(corners[0][0][1][1])
    
    if (x2==x1):
        x1=x2+0.000000001

    angle = ((math.atan2((y2-y1),(x2-x1)))*180)/math.pi
    
    return(angle)
