import numpy as np
import scipy
import time
from scipy import ndimage

"""
   considers number of 26 connected objects in the foreground and 6
   connected objects in the background should be equal
   before and after removal of border voxel (1) for
   deleting it (making it 0)

   before skeletonizing the image is thickened by using different
   structuring elements to avoid removal of entire even structure
   which did not seem to work

   reduces a cube to a single point
   lines - good
   circles/donuts - disconnected
   smaller circles - removes everything (even if thickened)


    refer to this link to understand why counting of objects is done 
    repeatedly using diferent structuring elements
    https://books.google.com/books?id=4Yz3gLkISnwC&pg=PA97&lpg=PA97&dq=Three-dimensional+simple+points:
    +Serial+erosion,+parallel+thinning+and+skeletonization&source
    =bl&ots=tvkyIAxZTP&sig=4lF1FxRKKwLIC-oyl_ikX4iNPts&hl=en&sa=X&ved=0CDgQ6AEwBGoVChMIlOvh9uKIyAIVki-ICh39tQd6#v=onepage&q=
    Three-dimensional%20simple%20points%3A%20Serial%20erosion%2C%20parallel%20thinning%20and%20skeletonization&f=false
    and to see how label works here http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.measurements.label.html


"""


def countObjects(inputImb, inputIma, se):
    """
    function to count number of objects
    in background and foreground
    """
    lb, obefore = scipy.ndimage.measurements.label(inputImb)
    lbc, ocbefore = scipy.ndimage.measurements.label(1 - inputImb)
    la, oafter = scipy.ndimage.measurements.label(inputIma)
    lac, ocafter = scipy.ndimage.measurements.label(1 - inputIma)

    if obefore == oafter and ocbefore == ocafter:
        deletableTemp = 1
    else:
        deletableTemp = 0

    return deletableTemp


def setStructureTrueOrFalse(a):
    """
    decide if the 3 by 3 by 3 structure
    is deletable
    """
    inputIma = np.copy(a)
    inputImb = np.copy(a)
    ndims = np.ndim(a)
    if ndims == 2:
        inputImb[1][1] = 1
        inputIma[1][1] = 0
        sElement = np.ones((3, 3), dtype=np.uint8)
        deletableTemp = countObjects(inputImb, inputIma, sElement)
    else:
        inputImb[1][1][1] = 1
        inputIma[1][1][1] = 0
        sElement = ndimage.generate_binary_structure(3, 3)
        deletableTemp = countObjects(inputImb, inputIma, sElement)
    return deletableTemp


def getBoundariesOfimage(image):
    """
    find edges by using erosion
    """
    if np.ndim(image) == 2:
        sElement = ndimage.generate_binary_structure(2, 1)
    else:
        sElement = ndimage.generate_binary_structure(3, 1)
    erode_im = scipy.ndimage.morphology.binary_erosion(image, sElement)
    b = image - erode_im
    return b


def getPaddedimage(image):
    """
    pad the image on all its
    boundaries with zeros
    """
    z, m, n = np.shape(image)
    paddedShape = z + 2, m + 2, n + 2
    padImage = np.zeros((paddedShape), dtype=np.uint8)
    padImage[1:z + 1, 1:m + 1, 1:n + 1] = image
    return padImage


def skeletonPass(image):
    """
    comprises single pass of removing borer points/edges
    """
    z, m, n = np.shape(image)
    paddedShape = z, m, n
    temp_del = np.ones((paddedShape), dtype=np.uint8)
    result = np.ones((paddedShape), dtype=np.uint8)
    b = getBoundariesOfimage(image)
    acopy = image.copy()
    numpixel_removed = 0
    for k in range(1, z - 1):
        for i in range(1, m - 1):
            for j in range(1, n - 1):
                if b[k, i, j] != 1:
                    continue
                asub = acopy[k - 1: k + 2, i - 1: i + 2, j - 1: j + 2]
                delOrNot = setStructureTrueOrFalse(asub)  # if edge pixel is 1
                if delOrNot != 0:
                    temp_del[k, i, j] = 0
                    numpixel_removed += 1
            acopy = np.multiply(acopy, temp_del)  # multiply the binary image with temp_del(image that marks edges as zeros)
            acopy = np.uint8(acopy)
    result[:] = acopy[:]
    return numpixel_removed, result


def getSkeletonize(image, sElement):
    """
    function to skeletonize a 2D or a 3D binary image with object in brighter contrast
    than background. In other words, 1 = object, 0 = background,iteratively
    continues until a topologically conencted single pixel wide curve is obtained
    sElement is the structuring element to dilate/thicken the image before
    thinning/skeletonizing

    """
    assert image.ndim in [2, 3]
    assert image.max() == 1
    assert image.min() >= 0
    assert image.dtype == np.uint8
    image = ndimage.binary_dilation(image, sElement)
    image = np.uint8(image)
    z, m, n = np.shape(image)
    padImage = getPaddedimage(image)
    start_skeleton = time.time()
    pass_no = 0
    numpixel_removed = 0
    numpixel_removedList = []
    while pass_no == 0 or numpixel_removed > 0:
        numpixel_removed, padImage = skeletonPass(padImage)
        print("number of pixels removed in pass", pass_no, "is ", numpixel_removed)
        numpixel_removedList.append(numpixel_removed)
        pass_no += 1
    print("done %i number of pixels in %i seconds" % (np.sum(image), time.time() - start_skeleton))
    return padImage[1:z + 1, 1:m + 1, 1:n + 1]


def getRing(ri, ro, size=(25, 25)):
    """
    Make a annular ring in 2d.
    The inner and outer radius are given as a
    percentage of the overall size.
    """
    n, m = size
    xs, ys = np.mgrid[-1:1:n * 1j, -1:1:m * 1j]
    r = np.sqrt(xs ** 2 + ys ** 2)

    torus = np.zeros(size, dtype=np.uint8)
    torus[(r < ro) & (r > ri)] = 1
    return torus


def getDonut(width=2, size=(25, 25, 25)):
    """
    three dimensional ring == donut
    """
    x, y, z = size
    assert width < z / 2

    # This is a single planr slice of ring
    ringPlane = getRing(0.25, 0.5, size=(x, y))

    # Stack up those slices starting form the center
    donutArray = np.zeros(size, dtype=np.uint8)
    zStart = z // 2
    for n in range(width):
        donutArray[zStart + n, :, :] = ringPlane

    return donutArray


if __name__ == '__main__':

    sampleCube = getDonut(2, (6, 6, 6))
    sElement = ndimage.generate_binary_structure(3, 3)
    resultCube1 = getSkeletonize(sampleCube, sElement)
    sElement = ndimage.generate_binary_structure(3, 1)
    resultCube2 = getSkeletonize(sampleCube, sElement)
    sElement = ndimage.generate_binary_structure(3, 2)
    resultCube3 = getSkeletonize(sampleCube, sElement)
    resultCube = np.logical_or(resultCube1, resultCube2)
    rc = np.logical_or(resultCube, resultCube3)
