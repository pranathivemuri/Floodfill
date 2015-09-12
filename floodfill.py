import numpy as np
import itertools
import scipy.ndimage

# see how label works here http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.measurements.label.html

def getAllnBitNumbers(n):
    """Generate all n bit binary sequences possible
    """
    x = [0, 1]
    # All possible binary configurations
    b = [p for p in itertools.product(x, repeat=n)]
    return b


def extractTemp(ndims):
    """  function to return the templates and number of templates
    """
    # take in a binary sequence and rearrange it to a an array 

    listOfBin = getAllnBitNumbers(pow(3, ndims))
    count = 0
    tempList = []
    for item in listOfBin:
        # convert the binary sequence to an array
        if ndims == 2:
            sizeIm = (3, 3)
            inputIm = np.reshape(item,sizeIm)
            inputIm[1][1] = 1
            se = np.ones((3, 3), dtype=np.uint8)
        else:
            sizeIm = (3, 3, 3)
            inputIm = np.reshape(item,sizeIm)
            inputIm[1][1][1] = 1
            se = np.ones((3, 3, 3), dtype=np.uint8)
        # label the 3 by 3 array before deleting the center pixel and count the number of objects based on first ordered neighborhood
        l,obefore = scipy.ndimage.measurements.label(inputIm, se)
        if ndims == 2:
            inputIm[1][1] = 0
        else:
            inputIm[1][1][1] = 0
        # label the 3 by 3 array after deleting the center pixel and count the number of objects based on first ordered neighborhood
        l,oafter = scipy.ndimage.measurements.label(inputIm, se)
        if obefore != oafter:
            tempList.append(inputIm)
            print(len(tempList))
    return tempList, len(tempList)

if __name__ == '__main__':
    templates, numOftemps = extractTemp(2)
    # must return 32
    # but doesn't gives 248
    # determine a better way to find connected objects
    # assert numOftemps == 32
