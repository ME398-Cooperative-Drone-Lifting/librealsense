import numpy as np

def Center(corners):
    center_array = np.round(np.mean(corners[0][0], axis=0))
    out_tuple = (int(center_array[0]),int(center_array[1]))
    return out_tuple
