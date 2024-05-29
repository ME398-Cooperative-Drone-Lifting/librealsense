import numpy as np

def Center(corners):
    center_array = np.round(np.mean(corners[0][0], axis=0))
    out_tuple = (int(center_array[0]),int(center_array[1]))
    return out_tuple




    '''
    xsum = 0
    ysum = 0
    count = 0
    for corner in corners:
        print(type(corner))
        print(corner)
        xsum += corner[0]
        ysum += corner[1]
        count += 1
    if count != 4:
        raise Exception("UNEXPECTED NUMBER OF CORNERS")
    return ((xsum/count, ysum/count))
    '''