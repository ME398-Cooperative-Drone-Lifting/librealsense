import pyrealsense2 as rs
import numpy as np
import cv2
import time
import math
from arucoHelpers_mult import CreateDetector, GetRelativeYaw
from realsenseStartup_mult import StartRealSense
from vectorHelpers_mult import Center

(arucoDict, arucoParams, detector) = CreateDetector()
(pipeline,align) = StartRealSense()

imageResized = False

try:
    while True: 
        # Wait for a coherent pair of frames: depth and infrared
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        ir_frame = frames.get_infrared_frame(1)  # 1 for the first infrared sensor

        if not depth_frame or not ir_frame:
            continue

        # Initialize aligned_frames to None
        aligned_frames = None

        # Initialize aligned_depth_frame to None
        aligned_depth_frame = None

        try:
            aligned_frames = align.process(frames)
            aligned_depth_frame = aligned_frames.get_depth_frame()
        except Exception as e:
            print("Error during alignment:", str(e))

        # Only proceed if aligned_depth_frame is not None and we have a valid aligned depth frame
        if aligned_depth_frame is not None and aligned_depth_frame:
            # Now we can safely get the intrinsic parameters
            depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())

        ir_image = np.asanyarray(ir_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        ir_colormap_dim = ir_image.shape

        num_rows = depth_image.shape[0]
        num_cols = depth_image.shape[1]

        # Only proceed if aligned_depth_frame is not None and we have a valid aligned depth frame
        if aligned_depth_frame is not None and aligned_depth_frame:
            # Now we can safely get the intrinsic parameters
            depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
        else:
            continue  # Skip the rest of the loop if we don't have a valid aligned depth frame

        # If depth and infrared resolutions are different, resize infrared image to match depth image for display
        if depth_colormap_dim != ir_colormap_dim:
            resized_ir_image = cv2.resize(ir_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            # Convert the resized infrared image to 3D by adding an extra dimension
            resized_ir_image = cv2.cvtColor(resized_ir_image, cv2.COLOR_GRAY2BGR)
            images = np.hstack((resized_ir_image, depth_colormap))
            imageResized = True
        else:
            # Convert the infrared image to 3D by adding an extra dimension
            ir_image = cv2.cvtColor(ir_image, cv2.COLOR_GRAY2BGR)
            images = np.hstack((ir_image, depth_colormap))
            imageResized = False

        if imageResized:
            arucoimage = resized_ir_image
        else:
            arucoimage = ir_image

        # Convert arucoimage to grayscale if it's not already
        if len(arucoimage.shape) == 3:
            arucoimage = cv2.cvtColor(arucoimage, cv2.COLOR_BGR2GRAY)

        # Detect ArUco markers
        (corners, ids, rejected) = cv2.aruco.detectMarkers(arucoimage, arucoDict, parameters=arucoParams)

        # Check if at least one marker was detected
        if ids is not None and len(ids) > 0:
            # Iterate over each detected marker
            for i in range(len(ids)):
                # Get the corners of the current marker
                markerCorners = corners[i][0]

                # Check if markerCorners is not empty
                if markerCorners.size > 0:
                    # Calculate the center of the current marker
                    marker_center = Center(markerCorners)

                    # Draw the corners and center of the current marker
                    markedImage = cv2.aruco.drawDetectedMarkers(arucoimage, [corners[i]], np.array([ids[i]]))                    
                    cv2.circle(markedImage, tuple(marker_center), 5, (0, 0, 255), cv2.FILLED)

                    # Get the depth of the current marker
                    depth = aligned_depth_frame.get_distance(*marker_center)

                    # Get the 3D coordinates of the current marker
                    depth_point_in_meters_camera_coords = rs.rs2_deproject_pixel_to_point(depth_intrin, marker_center, depth)

                    # Get the yaw of the current marker
                    angle = GetRelativeYaw(markerCorners)

                    print("\nMarker ID:", ids[i])
                    print("Corners:", markerCorners)
                    print("Center:", marker_center)
                    print("Coordinate in camera frame:", depth_point_in_meters_camera_coords)
                    print("Angle:", angle)

            # displaying aruco marked image
            markedImage = cv2.cvtColor(markedImage, cv2.COLOR_GRAY2BGR)
            disp_image = np.hstack((markedImage, depth_colormap))
        else:
            # Convert the infrared image to 3D by adding an extra dimension
            if imageResized:
                disp_image = np.hstack((resized_ir_image, depth_colormap))
            else:
                disp_image = np.hstack((ir_image, depth_colormap))

        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', disp_image)
        cv2.waitKey(10)
           
finally:
    # Stop streaming
    pipeline.stop()
