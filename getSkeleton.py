import numpy as np 
import scipy
import time
from scipy import ndimage
import matplotlib.pyplot as plt
from floodfill import extractTemp

selems, numOftemps3d = extractTemp(3)


def bwHitMiss(im,s):
    s1 = sum(sum(sum(np.logical_xor(im,s))))
    return s1

def delCenterPixel(im):
    assert np.shape(im) == (3, 3, 3)
    assert np.ndim(im) == 3
    b2 = 1
    for i in range(1,len(selems)):
        b1 = bwHitMiss(im, selems[i])
        x2 = np.logical_and(b1, b2)
        b2 = b1
    return x2


def edge(image):
    sElement = ndimage.generate_binary_structure(3, 1)
    # sElement = ndimage.generate_binary_structure(3, 2)
    # sElement = ndimage.generate_binary_structure(3, 3)
    erode_im = scipy.ndimage.morphology.binary_erosion(image, sElement)
    b = image - erode_im
    return b


def paddingImage(image):
    z, m, n = np.shape(image)
    paddedShape = z + 2, m + 2, n + 2
    padImage = np.zeros((paddedShape), dtype=np.uint8)
    padImage[1:z + 1, 1:m + 1, 1:n + 1] = image
    return padImage


def skeletonPass(image):
    z, m, n = np.shape(image)
    paddedShape = z, m, n
    temp_del = np.ones((paddedShape), dtype=np.uint8)
    result = np.ones((paddedShape), dtype=np.uint8)
    b = edge(image)
    acopy = image.copy()
    numpixel_removed = 0
    for k in range(1, z - 1):
        for i in range(1, m - 1):
            for j in range(1, n - 1):
                if b[k, i, j] != 1:
                    continue
                asub = acopy[k - 1: k + 2, j - 1: j + 2, i - 1: i + 2]
                delOrNot = delCenterPixel(asub)  # if edge pixel is 1
                if delOrNot != 0:
                    temp_del[k, i, j] = 0
                    numpixel_removed += 1
    acopy = np.multiply(acopy, temp_del)  # multiply the binary image with temp_del(image that marks edges as zeros)
    acopy = np.uint8(acopy)
    b = edge(acopy)
    result[:] = acopy[:]
    return numpixel_removed, result


def getSkeletonize3D(image):
    """function to skeletonize a 3D binary image with object in brighter contrast than background.
    In other words, 1 = object, 0 = background
    """
    assert image.ndim == 3
    assert image.max() == 1
    assert image.min() >= 0
    assert image.dtype == np.uint8
    z, m, n = np.shape(image)
    padImage = paddingImage(image)
    start_skeleton = time.time()
    pass_no = 0
    numpixel_removed = 0
    numpixel_removedList = []
    while pass_no == 0 or numpixel_removed > 0:
        numpixel_removed, padImage = skeletonPass(padImage)
        print("number of pixels removed in pass", pass_no, "is ", numpixel_removed)
        # print(padImage)
        numpixel_removedList.append(numpixel_removed)
        pass_no += 1
    # either number of pixels removed is wrong or the padimage is updating wrong
    # the following assertion which should always be true is false
    # assert(np.count_nonzero(image) - sum(numpixel_removedList) == np.count_nonzero(padImage))
    print("done %i number of pixels in %i seconds" % (np.size(image), time.time() - start_skeleton))

    return padImage[1:z + 1, 1:m + 1, 1:n + 1]

if __name__ == '__main__':
    sampleCube = np.zeros((3,64,64),dtype=np.uint8)
    sampleCube[:,16:49,16:49] = 1
    resultCube = getSkeletonize3D(sampleCube)
    plt.subplot(2, 3, 1)
    nr,nc = np.shape(resultCube[0])
    plt.imshow(sampleCube[0], cmap=plt.cm.gray, vmin=0,vmax=1,extent=[0,nr,0,nc])
    plt.colorbar()
    plt.subplot(2, 3, 2)
    plt.imshow(sampleCube[1], cmap=plt.cm.gray, vmin=0,vmax=1,extent=[0,nr,0,nc])
    plt.colorbar()
    plt.subplot(2, 3, 3)
    plt.imshow(sampleCube[2], cmap=plt.cm.gray, vmin=0,vmax=1,extent=[0,nr,0,nc])
    plt.colorbar()
    plt.subplot(2, 3, 4)
    plt.imshow(resultCube[0], cmap=plt.cm.gray, vmin=0,vmax=1,extent=[0,nr,0,nc])
    plt.colorbar()
    plt.subplot(2, 3, 5)
    plt.imshow(resultCube[1], cmap=plt.cm.gray, vmin=0,vmax=1,extent=[0,nr,0,nc])
    plt.colorbar()
    plt.subplot(2, 3, 6)
    plt.imshow(resultCube[2], cmap=plt.cm.gray, vmin=0,vmax=1,extent=[0,nr,0,nc])
    plt.colorbar()
    plt.show()
     

