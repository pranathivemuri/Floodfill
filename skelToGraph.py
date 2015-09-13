def binaryImageToGraph(npArray):
    # Basic binary array sanity checks
    assert npArray.ndim in [2, 3]
    assert npArray.dtype == np.uint8
    assert npArray.min() >= 0
    assert npArray.max() <= 1

    g = nx.Graph()
    cycles = []
    aShape = npArray.shape
    for coords, value in np.ndenumerate(npArray):
        # The point we start from must be "solid"
        if value != 1:
            continue

        # Check 1 step in each direction
        for d in range(npArray.ndim):
            # COnstruct the coordinate which is shifted
            # by 1 in the d'th dimension
            nearByCoordinate = list(coords)
            nearByCoordinate[d] += 1
            nearByCoordinate = tuple(nearByCoordinate)

            # Bounds check on the shifted coordinate
            if nearByCoordinate[d] == aShape[d]:
                continue
            # It it is solid, then assign an edge to that graph
            if npArray[nearByCoordinate] == 1:
                g.add_edge(coords, nearByCoordinate)
                cycles = len(nx.cycle_basis(g))
    return g, cycles


def floodfill(matrix, x, y):
    #"hidden" stop clause - not reinvoking for "c" or "b", only for "a".
    if matrix[x][y] == "1":  
        matrix[x][y] = "0" 
        #recursively invoke flood fill on all surrounding cells:
        if x > 0:
            floodfill(matrix,x-1,y)
        if x < len(matrix[y]) - 1:
            floodfill(matrix,x+1,y)
        if y > 0:
            floodfill(matrix,x,y-1)
        if y < len(matrix) - 1:
            floodfill(matrix,x,y+1)