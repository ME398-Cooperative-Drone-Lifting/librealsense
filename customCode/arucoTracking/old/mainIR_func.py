import pyrealsense2 as rs
import numpy as np
import cv2
# import time
# import math
from arucoHelpers_mult import CreateDetector, GetRelativeYaw
from realsenseStartup_mult import StartRealSense
from vectorHelpers_mult import Center

def get_frames(pipeline):
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    ir_frame = frames.get_infrared_frame(1)  # 1 for the first infrared sensor
    return frames, depth_frame, ir_frame

def align_frames(frames, align):
    aligned_frames = align.process(frames)
    aligned_depth_frame = aligned_frames.get_depth_frame()
    return aligned_depth_frame

def get_images(depth_frame, ir_frame):
    depth_image = np.asanyarray(depth_frame.get_data())
    ir_image = np.asanyarray(ir_frame.get_data())
    return depth_image, ir_image

def apply_colormap(depth_image):
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    return depth_colormap

def resize_ir_image(ir_image, depth_colormap_dim):
    resized_ir_image = cv2.resize(ir_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
    resized_ir_image = cv2.cvtColor(resized_ir_image, cv2.COLOR_GRAY2BGR)
    return resized_ir_image

def detect_markers(arucoimage, arucoDict, arucoParams):
    corners, ids, rejected = cv2.aruco.detectMarkers(arucoimage, arucoDict, parameters=arucoParams)
    return corners, ids, rejected

def process_markers(corners, ids, aligned_depth_frame, depth_intrin, arucoimage):
    for i in range(len(ids)):
        markerCorners = corners[i][0]
        if markerCorners.size > 0:
            marker_center = Center(markerCorners)
            markedImage = cv2.aruco.drawDetectedMarkers(arucoimage, [corners[i]], np.array([ids[i]]))                    
            cv2.circle(markedImage, tuple(marker_center), 5, (0, 0, 255), cv2.FILLED)
            depth = aligned_depth_frame.get_distance(*marker_center)
            depth_point_in_meters_camera_coords = rs.rs2_deproject_pixel_to_point(depth_intrin, marker_center, depth)
            angle = GetRelativeYaw(markerCorners)
            print("\nMarker ID:", ids[i])
            print("Corners:", markerCorners)
            print("Center:", marker_center)
            print("Coordinate in camera frame:", depth_point_in_meters_camera_coords)
            print("Angle:", angle)
    return markedImage

def display_image(disp_image):
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', disp_image)
    cv2.waitKey(10)

def main():
    (arucoDict, arucoParams, detector) = CreateDetector()
    (pipeline,align) = StartRealSense()

    print('RealSense camera activated...')

    imageResized = False
    stepCounter = 0

    try:
        while True:
            frames, depth_frame, ir_frame = get_frames(pipeline)
            if not depth_frame or not ir_frame:
                continue

            depth_intrin = depth_frame.get_profile().as_video_stream_profile().get_intrinsics()

            if stepCounter == 0:
                print('Frame pipeline successfully opened...')

            aligned_depth_frame = align_frames(frames, align)
            if aligned_depth_frame is None:
                continue

            depth_image, ir_image = get_images(depth_frame, ir_frame)
            depth_colormap = apply_colormap(depth_image)

            depth_colormap_dim = depth_colormap.shape
            ir_colormap_dim = ir_image.shape

            if depth_colormap_dim != ir_colormap_dim:
                resized_ir_image = resize_ir_image(ir_image, depth_colormap_dim)
                images = np.hstack((resized_ir_image, depth_colormap))
                imageResized = True
            else:
                ir_image = cv2.cvtColor(ir_image, cv2.COLOR_GRAY2BGR)
                images = np.hstack((ir_image, depth_colormap))
                imageResized = False

            if imageResized:
                arucoimage = resized_ir_image
            else:
                arucoimage = ir_image

            if len(arucoimage.shape) == 3:
                arucoimage = cv2.cvtColor(arucoimage, cv2.COLOR_BGR2GRAY)

            corners, ids, rejected = detect_markers(arucoimage, arucoDict, arucoParams)

            if ids is not None and len(ids) > 0:
                markedImage = process_markers(corners, ids, aligned_depth_frame, depth_intrin, arucoimage)
                markedImage = cv2.cvtColor(markedImage, cv2.COLOR_GRAY2BGR)
                disp_image = np.hstack((markedImage, depth_colormap))
            else:
                if imageResized:
                    disp_image = np.hstack((resized_ir_image, depth_colormap))
                else:
                    disp_image = np.hstack((ir_image, depth_colormap))

            # display_image(disp_image)

            stepCounter += 1

            # return vals of interest? log them somehow? TBD!
               
    finally:
        pipeline.stop()

if __name__ == "__main__":
    main()