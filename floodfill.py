import numpy as np
import itertools
import scipy.ndimage


def getAllnBitNumbers(n):
    """Generate all n bit binary sequences possible
    """
    x = [0, 1]
    # All possible binary configurations
    b = [p for p in itertools.product(x, repeat=n)]
    return b


def extractTemp():
    """  function to return the templates and number of templates
    """
    # take in a binary sequence and rearrange it to a an array 
    listOfBin = getAllnBitNumbers(9)
    for item in listOfBin:
        # convert the binary sequence to an array
        inputIm = np.reshape(item,(3,3))
        inputIm[1][1] = 
        # label the 3 by 3 array before deleting the center pixel and count the number of objects based on first ordered neighborhood
        l,obefore = scipy.ndimage.measurements.label(inputIm)
        inputIm[1][1] = 0
        # label the 3 by 3 array after deleting the center pixel and count the number of objects based on first ordered neighborhood
        l,oafter = scipy.ndimage.measurements.label(inputIm)
        tempList = []
        if obefore != oafter:
            tempList.append(inputIm)
    return tempList, len(tempList)

