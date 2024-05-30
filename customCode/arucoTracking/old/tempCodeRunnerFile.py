
                if np.abs(x*100) < 3 and np.abs(y*100) < 3:
                    print("Descend")
                else:
                    if x < 0:
                        print("Move Left: " + str(np.around(np.abs(x*100), 2)) + " cm")
                    if x > 0:
                        print("Move Right: " + str(np.around(np.abs(x*100),2)) + " cm")
                    if y < 0:
                        print("Move Up: " + str(np.around(np.abs(y*100),2)) + " cm")
                    if y > 0:
                        print("Move Down: " + str(np.around(np.abs(y*100), 2)) + " cm")
                print('-----------------')
                counter =0
        

            #See datasheet for information on coord system origin, p.97
            #https://dev.intelrealsense.com/docs/intel-realsense-d400-series-product-family-datasheet

            #displaying aruco marked image
            disp_image = np.hstack((markedImage, depth_colormap))
            
        else:
            disp_image = np.hstack((color_image, depth_colormap))
        
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', disp_image)
        cv2.waitKey(10)

        #wait for user input before reading next frame 
        #temp = input("Type quit to exit, press enter to load next frame\n")
        #if temp == "quit":
        #    break
        #time.sleep(15)
        #break
           
finally:

    # Stop streaming
    pipeline.stop()

