import pyrealsense2 as rs
import numpy as np
import cv2
from aruco_helpers import CreateDetector
from realsense_startup import StartRealSense
from vector_helpers import Center

(arucoDict, arucoParams, detector) = CreateDetector()
(pipeline,align) = StartRealSense()

imageResized = False

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        aligned_frames = align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()

        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        num_rows = depth_image.shape[0]
        num_cols = depth_image.shape[1]

        depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
            imageResized = True
        else:
            images = np.hstack((color_image, depth_colormap))
            imageResized = False



        if imageResized:
            arucoimage = resized_color_image
        else:
            arucoimage = color_image

        (corners, ids, rejected) = cv2.aruco.ArucoDetector.detectMarkers(detector, arucoimage)
        print("corners")
        print(corners)
        print("IDs")
        print(ids)

        # Show images
        ''' Default viewer
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        '''
        
        if ids != None:   
            #marking corners and center of aruco
            markedImage = cv2.aruco.drawDetectedMarkers(arucoimage, corners, ids)
            marker_center = Center(corners)
            cv2.circle(arucoimage,marker_center,5,(0,0,255), cv2.FILLED)



            depth = aligned_depth_frame.get_distance(*marker_center)
            POI = [marker_center[0], marker_center[1]]
            depth_point_in_meters_camera_coords = rs.rs2_deproject_pixel_to_point(depth_intrin, POI, depth)
            #Primary example referenced in realsense startup file comment, other example here: https://github.com/IntelRealSense/librealsense/issues/1413
            # Documentation on projection in general here



            print("\ncenter", marker_center)
            print("\ncoordinate in camera frame", depth_point_in_meters_camera_coords) 
            #See datasheet for information on coord system origin, p.97
            #https://dev.intelrealsense.com/docs/intel-realsense-d400-series-product-family-datasheet

            #displaying aruco marked image
            disp_image = np.hstack((markedImage, depth_colormap))

            #wait for user input before reading next frame
            '''
            temp = input("Type quit to exit, press enter to load next frame\n")
            if temp == "quit":
                break
            '''
        else:
            disp_image = np.hstack((color_image, depth_colormap))
        
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', disp_image)
        cv2.waitKey(1000)

           

finally:

    # Stop streaming
    pipeline.stop()

