import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport sqrt

cdef class BackgroundSubtractor:

    cdef bint useMorphology
    cdef int width, height, K
    cdef float alpha, threshold, STDDEVSQR
    
    cdef float[:, :, :] weights
    cdef float[:, :, :, :] means
    cdef float[:, :, :] variances

    def __init__(self, int width, int height, int K, float alpha, float threshold, bint useMorphology):
        self.width = width
        self.height = height
        self.K = K
        self.alpha = alpha
        self.threshold = threshold
        self.STDDEVSQR = 2.5**2
        self.useMorphology
        
        # Initialize the state for every pixel at once
        self.weights = np.zeros((self.height, self.width, self.K), dtype=np.float32)
        self.means = np.zeros((self.height, self.width, self.K, 3), dtype=np.float32)
        self.variances = np.ones((self.height, self.width, self.K), dtype=np.float32) * 30.0

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef apply(self, unsigned char[:, :, :] frame):
        maskNP = np.zeros((self.height, self.width), dtype=np.uint8)
        cdef unsigned char[:, :] maskView = maskNP
        cdef int y, x

        for y in range(self.height):
            for x in range(self.width):
                maskView[y, x] = self._processPixel(y, x, frame[y, x, :])

        if self.useMorphology:
            maskView = self.morph(maskView, 1) # Erode
            maskView = self.morph(maskView, 0) # Dilate

            maskView = self.morph(maskView, 0) # Dilate
            maskView = self.morph(maskView, 1) # Erode

        return maskNP

    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.cdivision(True)
    cdef inline int _processPixel(self, int y, int x, unsigned char[:] pixel):
        cdef int k, m, c
        cdef float b = <float>pixel[0]
        cdef float g = <float>pixel[1]
        cdef float r = <float>pixel[2]
        cdef float distSq, rho, totalW, weightSum
        cdef bint matched = False
        cdef int matchedIDx = -1

        # Add the pixel immediately to Initialize if non exist
        if self.weights[y, x, 0] == 0.0:
            self.weights[y, x, 0] = 1.0
            self.means[y, x, 0, 0] = b
            self.means[y, x, 0, 1] = g
            self.means[y, x, 0, 2] = r
            return 0

        # Update Weights, Means and Variances
        totalW = 0.0
        for k in range(self.K):
            distSq = (b - self.means[y, x, k, 0])**2 + (g - self.means[y, x, k, 1])**2 + (r - self.means[y, x, k, 2])**2

            # Update All Paramaters
            if not matched and distSq < (self.STDDEVSQR * self.variances[y, x, k]):
                matched = True
                matchedIDx = k
                self.weights[y, x, k] = (1.0 - self.alpha) * self.weights[y, x, k] + self.alpha

                for c in range(3):
                    self.means[y, x, k, c] = (1.0 - self.alpha) * self.means[y, x, k, c] + self.alpha * pixel[c]

                self.variances[y, x, k] = (1.0 - self.alpha) * self.variances[y, x, k] + self.alpha * distSq
                
            # Update only weights
            else:
                self.weights[y, x, k] = (1.0 - self.alpha) * self.weights[y, x, k]

            totalW += self.weights[y, x, k]

        # Save as new Gaussian Model if not matched
        if not matched:
            matchedIDx = 0
            for k in range(1, self.K):
                if self.weights[y, x, k] < self.weights[y, x, matchedIDx]:
                    matchedIDx = k

            self.means[y, x, matchedIDx, 0] = b
            self.means[y, x, matchedIDx, 1] = g
            self.means[y, x, matchedIDx, 2] = r
            self.variances[y, x, matchedIDx] = 30.0
            self.weights[y, x, matchedIDx] = self.alpha

            totalW = 0.0
            for k in range(self.K): 
                totalW += self.weights[y, x, k]
        
        # Normalize
        cdef float inverseW = 1.0 / totalW
        for k in range(self.K):
            self.weights[y, x, k] *= inverseW

        # Bubble Sort
        for k in range(self.K):
            for m in range(0, self.K - k - 1):
                if (self.weights[y, x, m] / sqrt(self.variances[y, x, m] + 1e-6) < self.weights[y, x, m+1] / sqrt(self.variances[y, x, m+1] + 1e-6)):
                    
                    self.weights[y, x, m], self.weights[y, x, m+1] = self.weights[y, x, m+1], self.weights[y, x, m]
                    self.variances[y, x, m], self.variances[y, x, m+1] = self.variances[y, x, m+1], self.variances[y, x, m]
                    
                    for c in range(3):
                        self.means[y, x, m, c], self.means[y, x, m+1, c] = self.means[y, x, m+1, c], self.means[y, x, m, c]
                    
                    if matchedIDx == m: 
                        matchedIDx = m + 1
                    elif matchedIDx == m + 1: 
                        matchedIDx = m

        # Background filtering
        weightSum = 0.0

        if not matched:
            return 255

        for k in range(self.K):
            weightSum += self.weights[y, x, k]

            if k == matchedIDx: 
                return 0

            if weightSum > self.threshold: 
                break

        return 255

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef unsigned char[:, :] morph(self, unsigned char[:, :] mask, int operation):
        cdef int h = mask.shape[0]
        cdef int w = mask.shape[1]
        cdef int y, x, ky, kx
        cdef bint hit
        
        # Create a Pointer to properly modify
        outNP = np.zeros((h, w), dtype=np.uint8)
        cdef unsigned char[:, :] out = outNP

        for y in range(2, h - 2):
            for x in range(2, w - 2):
                
                # OPERATION 0: Dilation (OR logic)
                if operation == 0:
                    hit = False
                    for ky in range(-2, 3):
                        for kx in range(-2, 3):
                            if mask[y + ky, x + kx] == 255:
                                hit = True
                                break
                    out[y, x] = 255 if hit else 0

                # OPERATION 1: Erosion (AND logic)
                elif operation == 1:
                    hit = True
                    for ky in range(-2, 3):
                        for kx in range(-2, 3):
                            if mask[y + ky, x + kx] == 0:
                                hit = False
                                break
                    out[y, x] = 255 if hit else 0
                    
        return out