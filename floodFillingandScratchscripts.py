import numpy as np
import itertools
import scipy.ndimage
import time

"""
filtering templates based on distances, number of objects 
and other trials at floodfilling which did not succeed as much
counter to count number of times a function is called is done
using a decorator and is in this program for reference

args and kwargs importance - http://stackoverflow.com/questions/3394835/args-and-kwargs
"""


def getAllnBitNumbers(n):
    """Generate all n bit binary sequences possible
    """
    x = [0, 1]
    # All possible binary configurations
    b = [p for p in itertools.product(x, repeat=n)]
    return b

# def bwHitMiss(im,s):
#     s1 = sum(sum(sum(np.logical_xor(im,s))))
#     return s1

# def delCenterPixel(im):
#     assert np.shape(im) == (3, 3, 3)
#     assert np.ndim(im) == 3
#     b2 = 1
#     for i in range(1,len(selems)):
#         b1 = bwHitMiss(im, selems[i])
#         x2 = np.logical_and(b1, b2)
#         b2 = b1
#     return x2


# def filterFloodFilltemps(inputIma, inputImb, se):
#     l, obefore = scipy.ndimage.measurements.label(inputImb, se)
#     l, oafter = scipy.ndimage.measurements.label(inputIma, se)
#     if obefore == oafter:
#         valOrNot = True
#     else:
#         valOrNot = False
#     return valOrNot


# def floodFillShortcut(ndims):
#     term = pow(ndims, ndims) - 1
#     listOfBin = getAllnBitNumbers(pow(2, term))
#     tempList = []
#     validBinseq = []
#     for item in listOfBin:
#         item = list(item)
#         # convert the binary sequence to an array
#         if ndims == 2:
#             index = 4
#             item.insert(index, 1)
#             sizeIm = (3, 3)
#             inputImb = np.reshape(item, sizeIm)
#             inputIma = np.reshape(item, sizeIm)
#             inputImb[1][1] = 0
#             inputIma[1][1] = 1
#         else:
#             index = 13
#             item.insert(index, 1)
#             sizeIm = (3, 3, 3)
#             inputImb = np.reshape(item, sizeIm)
#             inputIma = np.reshape(item, sizeIm)
#             inputImb[1][1][1] = 0
#             inputIma[1][1][1] = 1
#         nonZeroCoordsBefore = list(np.transpose(np.nonzero(inputImb)))
#         nonZeroCoordsAfter = list(np.transpose(np.nonzero(inputIma)))
#         distListBefore = []
#         distListAfter = []
#         for i in range(0, len(nonZeroCoordsBefore) - 1):
#             dist = np.linalg.norm(nonZeroCoordsBefore[i] - nonZeroCoordsBefore[i + 1])
#             dist = np.float32(dist)
#             distListBefore.append(dist)
#         for i in range(0, len(nonZeroCoordsAfter) - 1):
#             dist = np.linalg.norm(nonZeroCoordsAfter[i] - nonZeroCoordsAfter[i + 1])
#             dist = np.float32(dist)
#             distListAfter.append(dist)
#         unionOfLists = list(set(distListBefore) | set(distListAfter))
#         if set(unionOfLists) < set(distListBefore):
#             tempList.append(inputIma)
#             validBinseq.append(item)
#         print(len(tempList))
#     return tempList, len(tempList)


def extractTemp(ndims):
    """  function to return the templates and number of templates
    """
    # take in a binary sequence and rearrange it to a an array
    term = pow(ndims, ndims) - 1
    listOfBin = getAllnBitNumbers(pow(2, term))
    count = 0
    tempList = []
    tempListB = []
    for item in listOfBin:
        item = list(item)
        itemCopy = item.copy()
        # convert the binary sequence to an array
        if ndims == 2:
            index = 4
            itemCopy.insert(index, 1)
            sizeIm = (3, 3)
            inputImb = np.reshape(itemCopy, sizeIm)
            inputImb[1][1] = 1
            se = np.ones((3, 3), dtype=np.uint8)
        else:
            index = 13
            itemCopy.insert(index, 1)
            sizeIm = (3, 3, 3)
            inputImb = np.reshape(itemCopy, sizeIm)
            inputImb[1][1][1] = 1
            se = np.ones((3, 3, 3), dtype=np.uint8)
        # label the 3 by 3 array before deleting the center pixel and count the number of objects based on first ordered neighborhood
        l, obefore = scipy.ndimage.measurements.label(inputImb, se)
        if ndims == 2:
            sizeIm = (3, 3)
            inputIma = np.reshape(itemCopy, sizeIm)
            inputIma[1][1] = 0
        else:
            sizeIm = (3, 3, 3)
            inputIma = np.reshape(itemCopy, sizeIm)
            inputIma[1][1][1] = 0
        # label the 3 by 3 array after deleting the center pixel and count the number of objects based on first ordered neighborhood
        l, oafter = scipy.ndimage.measurements.label(inputIma, se)
        valOrNot = filterFloodFilltemps(item)
        if obefore == oafter:
            tempListB.append(inputImb)
            if valOrNot:
                tempList.append(inputImb)
                print(len(tempList))
        count += 1
        print(count)
    return tempList, len(tempList), tempListB, len(tempListB)


# number of zeros in the binary number
def getNumZeros(binary_Sequence):
    """Compute the number of zeros in a sequence
    """
    no_zeros = len(binary_Sequence) - np.count_nonzero(binary_Sequence)  # number of zeros
    return no_zeros


def getNumTransitions(binary_Sequence):
    """number of zero to one transition in a binary sequence
    """
    # loop to count number of zero to one transitions in the array of 1st neighborhood
    T = 0  # initialize number of zero to one transitions
    for k in range(0, len(binary_Sequence)):
        m = (k + 1) % (len(binary_Sequence))
        if binary_Sequence[k] == 0 and binary_Sequence[m] == 1:  # zero to 1 transitions:
            T = T + 1  # increment T If there is a transition
    return T


def filterFloodFilltemps(item):
    """Valid configurations are those binary sequences of
    8 bit numbers around a pixel that should be deleted as
    they do not belong to the centerline.
    """

    numZeros = getNumZeros(item)
    numTransitions = getNumTransitions(item)
    if numTransitions == 1 and numZeros in range(2, 6):
        val = True
    else:
        val = False
    return val


# def floodFillShortcut(ndims):
#     term = pow(ndims, ndims) - 1
#     listOfBin = getAllnBitNumbers(pow(2, term))
#     count = 0
#     tempList = []
#     validBinseq = []
#     for item in listOfBin:
#         item = list(item)
#         # convert the binary sequence to an array
#         if ndims == 2:
#             index = 4
#             item.insert(index, 1)
#             sizeIm = (3, 3)
#             inputImb = np.reshape(item, sizeIm)
#             inputIma = np.reshape(item, sizeIm)
#             inputImb[1][1] = 0
#             inputIma[1][1] = 1
#             distList = [1, 1.4142135]
#             se = np.ones((3, 3), dtype=np.uint8)
#         else:
#             index = 13
#             item.insert(index, 1)
#             sizeIm = (3, 3, 3)
#             inputImb = np.reshape(item, sizeIm)
#             inputIma = np.reshape(item, sizeIm)
#             inputImb[1][1][1] = 0
#             inputIma[1][1][1] = 1
#             distList = [1, 1.4142135, 1.7320508]
#             se = np.ones((3, 3, 3), dtype=np.uint8)
#         a = list(np.transpose(np.nonzero(inputImb)))
#         distListBefore = []
#         # distListfiltered = []
#         for i in range(0, len(a) - 1):
#             dist = np.linalg.norm(a[i] - a[i + 1])
#             dist = np.float32(dist)
#             if dist not in distList:
#                 break
#             else:
#                 distListBefore.append(dist)
#         # v = list(set(distListBefore) & set(distList))
#         # if v is [1]:
#         #     distListfiltered = []
#         # else:
#         #     distListfiltered = distListBefore
#         for validityDists in distListBefore:
#             tempValidDelList = []
#             if validityDists in distList:
#                 tempValidDel = 1
#             else:
#                 tempValidDel = 0
#             tempValidDelList.append(tempValidDel)
#             if len(tempValidDelList) == len(distListBefore):
#                 valOrNot = filterFloodFilltemps(inputIma, inputImb, se)
#                 if valOrNot == 1:
#                     tempList.append(inputIma)
#                     validBinseq.append(item)
#                     print(len(tempList))
#             count += 1
#             print(count)
#     return tempList, len(tempList)


from functools import wraps

def counter(func):
    @wraps(func)
    def tmp(*args, **kwargs):
        tmp.count += 1
        return func(*args, **kwargs)
    tmp.count = 0
    return tmp

@counter
def floodfill(matrix, x, y):
    if matrix[x][y] == "1":
        # recursively invoke flood fill on all surrounding cells:
        if x > 0:
            floodfill(matrix, x - 1, y)
        if x < len(matrix[y]) - 1:
            floodfill(matrix, x + 1, y)
        if y > 0:
            floodfill(matrix, x, y - 1)
        if y < len(matrix) - 1:
            floodfill(matrix, x, y + 1)
    return matrix, floodfill.count
