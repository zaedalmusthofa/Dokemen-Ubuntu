import time

import cv2
import numpy as np
from multiprocessing import Pool


class PyramidBlendingMethod:
    '''
    Class that performs blending operations on images using pyramids.
    '''

    def __init__(self, depth=6):
        self.depth = depth
        self.final_mask = None
        self.lp1 = None
        self.lp2 = None
        self.mask1truth = None
        self.mask2truth = None

    def getGaussianPyramid(self, img):
        # For the image, downscale the image, and return an array.
        pyra = [img]
        for i in range(self.depth - 1):
            down = cv2.pyrDown(pyra[i])
            pyra.append(down)
        return pyra

    def pyr_down_up(self, img):
        nextImg = cv2.pyrDown(img)
        size = (img.shape[1], img.shape[0])
        up = cv2.pyrUp(nextImg, dstsize=size)
        return img.astype(np.float32) - up.astype(np.float32)

    def generate_pyramid(self, img):
        pyra = [img]
        for i in range(self.depth - 1):
            nextImg = cv2.pyrDown(pyra[-1])
            pyra.append(nextImg)
        return pyra

    def getLaplacianPyramid(self, img):
        # generate the Gaussian pyramid
        gauss_pyra = self.generate_pyramid(img)

        # compute the Laplacian pyramid
        lap_pyra = []
        for i in range(self.depth - 1):
            size = (gauss_pyra[i].shape[1], gauss_pyra[i].shape[0])
            up = cv2.pyrUp(gauss_pyra[i+1], dstsize=size)
            sub = gauss_pyra[i].astype(float) - up.astype(float)
            lap_pyra.append(sub)

        # append the last level of the Gaussian pyramid to the Laplacian pyramid
        lap_pyra.append(gauss_pyra[-1])

        return lap_pyra

    def getBlendingPyramid(self, lpa, lpb, gpm):
        # Blends the pyramid stages at each level according to the mask.
        # since the boundary of the mask changes at each downscaling,
        # we need to get the pyramid for the mask as well
        pyra = []
        for i, mask in enumerate(gpm):
            maskNet = cv2.merge((mask, mask, mask))
            blended = lpa[i] * maskNet + lpb[i] * (1 - maskNet)
            pyra.append(blended)

        return pyra

    def reconstruct(self, lp):
        # for each stage in the laplacian pyramid, reconstruct by adding (inverse of what we did when downscaling)
        img = lp[-1]
        for i in range(len(lp) - 2, -1, -1):
            laplacian = lp[i]
            size = laplacian.shape[:2][::-1]

            img = cv2.pyrUp(img, dstsize=size).astype(float)
            img += laplacian.astype(float)

        return img

    def getMask(self, img):
        # gets the mask of a particular image. Simply a helper function

        mask = img[:, :, 0] != 0
        mask = np.logical_and(img[:, :, 1] != 0, mask)
        mask = np.logical_and(img[:, :, 2] != 0, mask)

        maskImg = np.zeros(img.shape[:2], dtype=float)
        maskImg[mask] = 1.0
        return maskImg, mask

    def blend(self, img1, img2, strategy='STRAIGHTCUT'):
        '''
        Blends the two images by getting the pyramids and blending appropriately.
        '''

        # compupte the required pyramids
        self.final_mask = None
        start = time.time()
        self.lp1 = self.getLaplacianPyramid(img1)
        self.lp2 = self.getLaplacianPyramid(img2)
        # print("lp1, lp2 " + str(time.time() - start))
        if self.final_mask is None:
            # get the masks of both images.
            _, self.mask1truth = self.getMask(img1)
            _, self.mask2truth = self.getMask(img2)

            # using the overlaps of both the images, we compute the bounding boxes.

            overlap = self.mask1truth & self.mask2truth

            tempMask = np.zeros(img1.shape[:2])
            yb, xb = np.where(overlap)
            minx = np.min(xb)
            maxx = np.max(xb)
            miny = np.min(yb)
            maxy = np.max(yb)
            h, w = tempMask.shape

            Mask = np.zeros(img1.shape[:2])
            if strategy == 'STRAIGHTCUT':
                # simple strategy if there is only left -> right panning.
                Mask[:, :(minx + maxx) // 2] = 1.0
                self.final_mask = Mask
            elif strategy == 'DIAGONAL':
                # Strategy that allows for slight variations in vertical movement also
                self.final_mask = cv2.fillConvexPoly(Mask, np.array([
                    [
                        [minx, miny],
                        [maxx, maxy],
                        [maxx, h],
                        [0, h],
                        [0, 0],
                        [minx, 0]
                    ]
                ]), True, 50)

        else:
            pass
        gpm = self.getGaussianPyramid(self.final_mask)

        blendPyra = self.getBlendingPyramid(self.lp1, self.lp2, gpm)

        finalImg = self.reconstruct(blendPyra)

        return finalImg
