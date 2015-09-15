import numpy as np
import itertools
import time


def getAllnBitNumbers(n):
    """Generate all n bit binary sequences possible
    """
    x = [0, 1]
    # All possible binary configurations
    b = [p for p in itertools.product(x, repeat=n)]
    return b


def floodFillShortcut(ndims):
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
        nonZeroCoordsBefore = list(np.transpose(np.nonzero(inputImb)))
        nonZeroCoordsAfter = list(np.transpose(np.nonzero(inputIma)))
        unfilledBefore = len(nonZeroCoordsBefore)
        unfilledAfter = len(nonZeroCoordsAfter)
        objectsBefore = 0
        objectsAfter = 0
        while unfilledBefore > 0:
            inputImBfilled = floodfill(inputImb)
            objectsBefore = objectsBefore + 1
            unfilledBefore = len(list(np.transpose(np.nonzero(inputImBfilled))))
        while unfilledAfter > 0:
            inputImAfilled = floodfill(inputIma)
            objectsAfter = objectsAfter + 1
            unfilledAfter = len(list(np.transpose(np.nonzero(inputImAfilled))))
        if objectsBefore == objectsAfter:
            tempList.append(inputImb)
            validBinseq.append(item)
    return tempList, len(tempList)


def floodfill(matrix):
    # a function that fllodfills all possible 1s and also returns their coordinates
    # if there are no more UNFILLED 1s then number of objects are 1
    # return matrixFilled
    a = list(np.transpose(np.nonzero(matrix)))
    matrixFilled = np.zeros_like(matrix)
    adjToNZCoordList = []
    nonZeroCoordlist = []
    count = 0
    for i in a:
        nonZeroCoordlist.append(tuple(i))
        for coords in nonZeroCoordlist:
            # The point we start from must be "solid"
            # Check 1 step in each direction
            matrixFilled[coords] == 1
            nearByCoordinateList = []
            stepAllDirect = itertools.product((0, 1, 2), repeat=matrix.ndim)
            stepDirect = itertools.product((0, 1), repeat=matrix.ndim)
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
                    if nearByCoordinate not in nonZeroCoordlist:
                        val = False
                        count = count + 1
                    else:
                        val = True
                        count = count + 1
                if count == 2:
                    objCount = objCount + 1
    return objCount


if __name__ == '__main__':
    startt = time.time()
    templates2d, numOftemps2d = floodFillShortcut(2)
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
