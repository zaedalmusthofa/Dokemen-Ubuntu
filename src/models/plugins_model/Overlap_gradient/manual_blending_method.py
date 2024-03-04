import cv2
import numpy as np


class ManualBlendingMethod:
    def __init__(self):
        pass

    def create_mask_blending(self, img1, img2):
        G0, _ = self.get_weight_mask_matrix(img1, img2)
        return G0

    @classmethod
    def create_blending(cls, img1, img2, G0):
        if G0 is not None:
            weights = [np.stack((G, G, G), axis=2) for G in (G0, G0, G0, G0)]
            image_overlap = (img1 * weights[0] + img2 * (1 - weights[0])).astype(np.uint8)
        else:
            image_overlap = None
        return image_overlap

    def get_weight_mask_matrix(self, im1, im2, dist_threshold=1):
        """
        Get the weight matrix G that combines two images imA, imB smoothly.

        imA = image overlapping A
        imB = image Overlapping B
        """
        overlap_mask = self.get_overlap_region_mask(im1, im2)
        overlap_mask_inv = cv2.bitwise_not(overlap_mask)
        indices = np.where(overlap_mask == 255)
        imA_diff = cv2.bitwise_and(im1, im1, mask=overlap_mask_inv)
        imB_diff = cv2.bitwise_and(im2, im2, mask=overlap_mask_inv)
        # cv2.imwrite("imA_diff.jpg", imA_diff)
        G = self.get_mask(im1).astype(np.float32) / 255.0
        # cv2.imwrite("image.jpg", G)
        polyA = self.get_outermost_polygon_boundary(imA_diff)
        polyB = self.get_outermost_polygon_boundary(imB_diff)
        for y, x in zip(*indices):
            # pt = tuple([int(round(x)), int(round(y))])
            pt = (int(round(x)), int(round(y)))
            distToB = cv2.pointPolygonTest(polyB, pt, True)
            if distToB < dist_threshold:
                distToA = cv2.pointPolygonTest(polyA, pt, True)
                distToB *= distToB
                distToA *= distToA
                # G[y, x] = distToB / (distToA + distToB)
                if distToA == 0 and distToB == 0:
                    G[y, x] = 0
                else:
                    G[y, x] = distToB / (distToA + distToB)

        return G, overlap_mask

    def get_overlap_region_mask(self, im1, im2):
        """
        Given two images of the save size, get their overlapping region and
        convert this region to a mask array.
        """
        overlap = cv2.bitwise_and(im1, im2)
        mask = self.get_mask(overlap)
        # cv2.imwrite("mask2.jpg", mask)
        mask = cv2.dilate(mask, np.ones((2, 2), np.uint8), iterations=2)
        # cv2.imwrite("mask.jpg", mask)
        return mask

    def get_mask(self, img):
        """
        Convert an image to a mask array.
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
        return mask

    def get_outermost_polygon_boundary(self, img):
        """
        Given a mask image with the mask describes the overlapping region of
        two images, get the outermost contour of this region.
        """
        mask = self.get_mask(img)
        mask = cv2.dilate(mask, np.ones((2, 2), np.uint8), iterations=2)
        contours, hierarchy = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2:]

        # get the contour with the largest area
        C = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)[0]

        # polygon approximation
        polygon = cv2.approxPolyDP(C, 0.009 * cv2.arcLength(C, True), True)

        return polygon

    def crop_region(self, img, name):
        region_info = {
            "left": [[0, 0], [int(img.shape[1] * 2 / 3), 0], [int(img.shape[1] * 2 / 3), img.shape[0]], [0, img.shape[0]]],
            "right": [[img.shape[1], 0], [img.shape[1], img.shape[0]], [int(img.shape[1]/3), img.shape[0]], [int(img.shape[1]/3), 0]]
        }

        pts = np.array(region_info[name])
        return self.region_bounding(img, name, pts)

    def region_bounding(self, img, name, pts):
        rect = cv2.boundingRect(pts)
        x, y, w, h = rect
        cropped = img[y:y + h, x:x + w]

        pts = pts - pts.min(axis=0)

        mask = np.zeros(cropped.shape[:2], np.uint8)
        cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

        canvas = np.zeros([img.shape[0], img.shape[1], 3], dtype=np.uint8)
        dst = cv2.bitwise_and(cropped, cropped, mask=mask)

        if name in ["left"]:
            canvas[0:0 + dst.shape[0], 0:0 + dst.shape[1]] = dst
        elif name in ["right"]:
            canvas[0:dst.shape[0],
            canvas.shape[1] - dst.shape[1]:canvas.shape[1] - dst.shape[1] + dst.shape[1]] = dst

        return canvas
