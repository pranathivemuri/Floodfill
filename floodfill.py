import numpy as np
import itertools
# import scipy.ndimage
import time

# see how label works here http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.measurements.label.html


def getAllnBitNumbers(n):
    """Generate all n bit binary sequences possible
    """
    x = [0, 1]
    # All possible binary configurations
    b = [p for p in itertools.product(x, repeat=n)]
    return b


def floodFill(ndims):
    term = pow(ndims, ndims) - 1
    listOfBin = getAllnBitNumbers(pow(2, term))
    tempList = []
    validBinseq = []
    for item in listOfBin:
        item = list(item)
        # convert the binary sequence to an array
        if ndims == 2:
            index = 4
            item.insert(index, 1)
            sizeIm = (3, 3)
            inputImb = np.reshape(item, sizeIm)
            inputIma = np.reshape(item, sizeIm)
            inputImb[1][1] = 0
            inputIma[1][1] = 1
        else:
            index = 13
            item.insert(index, 1)
            sizeIm = (3, 3, 3)
            inputImb = np.reshape(item, sizeIm)
            inputIma = np.reshape(item, sizeIm)
            inputImb[1][1][1] = 0
            inputIma[1][1][1] = 1
        obCount = templatesExtractfloodfill(inputImb)
        if obCount > 1:
            tempList.append(inputIma)
            validBinseq.append(item)
            print(len(tempList))
    return tempList, len(tempList)


def templatesExtractfloodfill(npArray):
    a = list(np.transpose(np.nonzero(npArray)))
    adjToNZCoordList = []
    nonZeroCoordlist = []
    count = 0
    for i in a:
        nonZeroCoordlist.append(tuple(i))
    for coords in nonZeroCoordlist:
        # The point we start from must be "solid"
        # Check 1 step in each direction
        nearByCoordinateList = []
        stepAllDirect = itertools.product((0, 1, 2), repeat=npArray.ndim)
        stepDirect = itertools.product((0, 1), repeat=npArray.ndim)
        listStepDirect = list(stepDirect)
        listStepAllDirect = list(stepAllDirect)
        listStepDirect = listStepDirect[1: len(listStepDirect) - 1]
        for d in listStepDirect:
            # COnstruct the coordinate which is shifted
            # by 1 in the d'th dimension
            nearByCoordinate = np.array(coords)
            nearByCoordinate = nearByCoordinate + np.array(d)
            nearByCoordinate = tuple(nearByCoordinate)
            if nearByCoordinate in listStepAllDirect:
                if nearByCoordinate in nonZeroCoordlist:
                    nearByCoordinateList.append(nearByCoordinate)
        adjToNZCoord = list(zip(coords, nearByCoordinateList))
        adjToNZCoordList.append(nearByCoordinateList)
                if npArray[nearByCoordinate] != 1:
                    count = count + 1
    print("num of objects in this template is", count)
    return count


# def filterFloodFilltemps(inputIma, inputImb, se):
#     l, obefore = scipy.ndimage.measurements.label(inputImb, se)
#     l, oafter = scipy.ndimage.measurements.label(inputIma, se)
#     if obefore == oafter:
#         valOrNot = True
#     else:
#         valOrNot = False
#     return valOrNot


# nearByCoordinateList.append(nearByCoordinate)
# uniqueNbc = list(set(nearByCoordinateList))
# validIncrements = list(set(uniqueNbc) & set(listStepAllDirect))

if __name__ == '__main__':
    startt = time.time()
    templates2d, numOftemps2d = floodFill(2)
    # templates3d, numOftemps3d = floodFillShortcut(3)
    thefile = open('test.txt', 'w')
    for item in templates2d:
        thefile.write("%s\n" % item)
    thefile.close()
    stop = time.time()
    print("time taken is", (stop - startt))
    # must return 32
    # but doesn't gives 124
    # determine a better way to find connected objects
    # assert numOftemps == 32
