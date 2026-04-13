import numpy as np
cimport numpy as np
cimport cython

DEF MAX_LABELS = 100000

cdef class ObjectTracker:

    cdef int[:] parent
    cdef int nextLabel

    def __init__(self):
        self.parent = np.zeros(MAX_LABELS, dtype=np.int32)

    cdef inline void makeSet(self, int x):
        self.parent[x] = x

    cdef int find(self, int x):
        cdef int root = x
        while root != self.parent[root]:
            root = self.parent[root]

        cdef int curr = x
        cdef int nxt
        while curr != root:
            nxt = self.parent[curr]
            self.parent[curr] = root
            curr = nxt

        return root

    cdef inline void union(self, int x, int y):
        cdef int rootX = self.find(x)
        cdef int rootY = self.find(y)

        if rootX != rootY:
            if rootX < rootY:
                self.parent[rootY] = rootX
            else:
                self.parent[rootX] = rootY        

    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.cdivision(True)
    cpdef list process(self, unsigned char[:, :] binaryMask):
        cdef int height = binaryMask.shape[0]
        cdef int width = binaryMask.shape[1]

        cdef int[:, :] labels = np.zeros((height, width), dtype=np.int32)

        cdef int y, x, top, left, minLabel
        self.nextLabel = 1
        self.makeSet(0)

        # Assign Temporary labels
        for y in range(height):
            for x in range(width):
                if binaryMask[y, x] == 255:
                    top = labels[y-1, x] if y > 0 else 0
                    left = labels[y, x-1] if x > 0 else 0

                    # New Component has been found
                    if top == 0 and left == 0:
                        if self.nextLabel < MAX_LABELS:
                            self.makeSet(self.nextLabel)
                            labels[y, x] = self.nextLabel
                            self.nextLabel += 1

                    # Connect to the Top
                    elif top != 0 and left == 0:
                        labels[y, x] = top
                    
                    # Connect to the Left
                    elif left != 0 and top == 0:
                        labels[y, x] = left

                    # Touching both top and left
                    else:
                        if top < left:
                            minLabel = top
                        else:
                            minLabel = left
                        
                        labels[y, x] = minLabel
                        self.union(top, left)
        
        # Flattent the labels to calculate bounding boxes
        cdef int[:] minX = np.full(self.nextLabel, width, dtype=np.int32)
        cdef int[:] minY = np.full(self.nextLabel, height, dtype=np.int32)
        cdef int[:] maxX = np.zeros(self.nextLabel, dtype=np.int32)
        cdef int[:] maxY = np.zeros(self.nextLabel, dtype=np.int32)
        cdef int[:] active = np.zeros(self.nextLabel, dtype=np.int32)

        cdef int trueLabel

        for y in range(height):
            for x in range(width):
                if labels[y, x] > 0:

                    trueLabel = self.find(labels[y, x])
                    active[trueLabel] = 1

                    if x < minX[trueLabel]: 
                        minX[trueLabel] = x
                    if y < minY[trueLabel]: 
                        minY[trueLabel] = y
                    if x > maxX[trueLabel]: 
                        maxX[trueLabel] = x
                    if y > maxY[trueLabel]: 
                        maxY[trueLabel] = y

        cdef list boundingBoxes = []
        cdef int w, h

        for i in range(1, self.nextLabel):
            if active[i] == 1:
                w = maxX[i] - minX[i]
                h = maxY[i] - minY[i]

                if w * h > 350:
                    boundingBoxes.append((minX[i], minY[i], w, h))

        return boundingBoxes
