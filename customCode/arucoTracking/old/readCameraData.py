import pyrealsense2 as rs
import numpy as np
import cv2
#from PIL import Image

#setup Aruco Detector and which marker
#arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50) #https://chev.me/arucogen/
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50) #https://chev.me/arucogen/

# we will use marker 0 of the dictionary, 50 cm^2
arucoParams = cv2.aruco.DetectorParameters() # use default detect params
#refParams = cv2.aruco.RefineParameters()
#detector = cv2.aruco.ArucoDetector(arucoDict,arucoParams,refParams)
detector = cv2.aruco.ArucoDetector(arucoDict,arucoParams)

imageResized = False

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("RGB Camera Not Found")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
            imageResized = True
        else:
            images = np.hstack((color_image, depth_colormap))
            imageResized = False

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)

        '''
        corners = []
        ids = np.array([])
        rejected = []
        ''' 

        if imageResized:
            arucoimage = resized_color_image
            #arucoimage = cv2.Mat(resized_color_image)
        #     #arucoimage = Image.fromarray(resized_color_image)
        #     #arucoimage = cv2.imdecode(resized_color_image, cv2.IMREAD_UNCHANGED)
        #     cv2.imwrite('temp_image.png',resized_color_image)
        else:
            arucoimage = color_image
            #arucoimage = cv2.Mat(color_image)
        #     #arucoimage = cv2.imdecode(color_image, cv2.IMREAD_UNCHANGED)
        #     #arucoimage = Image.fromarray(color_image)
        #     cv2.imwrite('temp_image.png',color_image)
        # #arucoimage = cv2.imdecode(arucoimage, cv2.IMREAD_UNCHANGED)
        # arucoimage = cv2.imread('temp_image.png')



        #(corners, ids, rejected) = cv2.aruco.ArucoDetector.detectMarkers(detector, arucoimage,arucoDict,parameters = arucoParams) #get corners of aruco markers
        (corners, ids, rejected) = cv2.aruco.ArucoDetector.detectMarkers(detector, arucoimage)        #if len(corners) == 1:
        print("corners")
        print(corners)
        print("IDs")
        print(ids)
        cv2.waitKey(1000)
        temp = input("continue?")
        if temp == "quit":
            break


            

finally:

    # Stop streaming
    pipeline.stop()