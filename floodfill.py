import numpy as np
import itertools
import scipy.ndimage
import time

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
    term = pow(ndims, ndims) - 1
    listOfBin = getAllnBitNumbers(pow(2, term))
    count = 0
    tempList = []
    for item in listOfBin:
        item = list(item)
        # convert the binary sequence to an array
        if ndims == 2:
            index = 4
            item.insert(index, 1)
            sizeIm = (3, 3)
            inputImb = np.reshape(item,sizeIm)
            inputImb[1][1] = 1
            se = np.ones((3, 3), dtype=np.uint8)
        else:
            index = 13
            item.insert(index, 1)
            sizeIm = (3, 3, 3)
            inputImb = np.reshape(item,sizeIm)
            inputImb[1][1][1] = 1
            se = np.ones((3, 3, 3), dtype=np.uint8)
        # label the 3 by 3 array before deleting the center pixel and count the number of objects based on first ordered neighborhood
        l,obefore = scipy.ndimage.measurements.label(inputImb, se)
        if ndims == 2:
            sizeIm = (3, 3)
            inputIma = np.reshape(item,sizeIm)
            inputIma[1][1] = 0
        else:
            sizeIm = (3, 3, 3)
            inputIma = np.reshape(item,sizeIm)
            inputIma[1][1][1] = 0
        # label the 3 by 3 array after deleting the center pixel and count the number of objects based on first ordered neighborhood
        l,oafter = scipy.ndimage.measurements.label(inputIma, se)
        if obefore == oafter:
            tempList.append(inputImb)
            print(len(tempList))
        count += 1
        print(count)
    return tempList, len(tempList)

if __name__ == '__main__':
    # templates2d, numOftemps2d = extractTemp(2)
    startt = time.time()
    templates3d, numOftemps3d = extractTemp(3)
    thefile = open('test.txt', 'w') 
    for item in templates3d:
        thefile.write("%s\n" % item)
    thefile.close()
    stop = time.time()
    print("time taken is", (stop - startt))
    # must return 32
    # but doesn't gives 248
    # determine a better way to find connected objects
    # assert numOftemps == 32
