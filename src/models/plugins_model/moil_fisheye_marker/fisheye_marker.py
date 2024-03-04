from typing import Tuple
import cv2
import numpy as np
import json


class MoilFisheyeMarker:

    @classmethod
    def __auto_thickness(cls, image: np.ndarray) -> int:
        h, w = image.shape[:2]
        if w >= h:
            return h // 350
        if h > w:
            return w // 350

    @classmethod
    def __auto_point_size(cls, image: np.ndarray) -> int:
        h, w = image.shape[:2]
        if w >= h:
            return h // 150
        if h > w:
            return w // 150

    @staticmethod
    # circle size flexible
    def point(image: np.ndarray,
              pixel_coordinate: Tuple[int, int],
              radius: int = None,
              color: tuple = (0, 0, 255),
              fill: bool = False) -> np.ndarray:
        """
        Draw a point mark on the image.

        :param image: np.ndarray
        :param pixel_coordinate: Tuple[x: int, y: int]
        :param radius: int (optional)
        :param color: Tuple[b: int, g: int, r: int]
        :param fill: bool
        :return: np.ndarray
        """

        x, y = pixel_coordinate

        if not radius:
            radius = MoilFisheyeMarker.__auto_point_size(image)

        thickness = MoilFisheyeMarker.__auto_thickness(image)
        if thickness == 0:
            thickness = 2

        if fill:
            cv2.circle(image, (x, y), radius=radius, color=color, thickness=-1)
        else:
            cv2.circle(image, (x, y), radius=radius, color=color, thickness=thickness)

        return image

    @staticmethod
    # circle position flexible
    def crosshair(image: np.ndarray,
                  pixel_coordinate: Tuple[int, int],
                  color: Tuple[int, int, int] = (0, 0, 255)) -> np.ndarray:
        """
        Draw a crosshair mark on the image.

        :param image: np.ndarray
        :param pixel_coordinate: Tuple[x: int, y: int]
        :param color: Tuple[b: int, g: int, r: int]
        :return: np.ndarray
        """

        x, y = pixel_coordinate

        size = MoilFisheyeMarker.__auto_point_size(image) * 3
        thickness = int(MoilFisheyeMarker.__auto_thickness(image) // 1.5)
        if thickness == 0:
            thickness = 2

        cv2.line(image, (x + size, y), (x - size, y), color, thickness)
        cv2.line(image, (x, y + size), (x, y - size), color, thickness)

        return image

    @staticmethod
    def cross(image: np.ndarray,
              pixel_coordinate: Tuple[int, int],
              color: Tuple[int, int, int] = (0, 0, 255)) -> np.ndarray:
        """
        Draw a cross mark on the image.

        :param image: np.ndarray
        :param pixel_coordinate: Tuple[x: int, y: int]
        :param color: Tuple[b: int, g: int, r: int]
        :return: np.ndarray
        """

        x, y = pixel_coordinate

        size = MoilFisheyeMarker.__auto_point_size(image)
        thickness = MoilFisheyeMarker.__auto_thickness(image)
        if thickness == 0:
            thickness = 2

        cv2.line(image, (x + size, y + size), (x - size, y - size), color, thickness)
        cv2.line(image, (x + size, y - size), (x - size, y + size), color, thickness)

        return image

    @staticmethod
    def square(image: np.ndarray,
              pixel_coordinate: Tuple[int, int],
              color: Tuple[int, int, int] = (0, 0, 255)) -> np.ndarray:
        """
        Draw a square mark on the image.

        :param image: np.ndarray
        :param pixel_coordinate: Tuple[x: int, y: int]
        :param color: Tuple[b: int, g: int, r: int]
        :return: np.ndarray
        """

        x = pixel_coordinate[0]
        y = pixel_coordinate[1]

        size = MoilFisheyeMarker.__auto_point_size(image)
        thickness = MoilFisheyeMarker.__auto_thickness(image)
        if thickness == 0:
            thickness = 2

        cv2.rectangle(image, (x + size, y + size), (x - size, y - size), color, thickness)

        return image

    @staticmethod
    def triangle(image: np.ndarray,
              pixel_coordinate: Tuple[int, int],
              color: Tuple[int, int, int] = (0, 0, 255)) -> np.ndarray:
        """
        Draw a triangle mark on the image.

        :param image: np.ndarray
        :param pixel_coordinate: Tuple[x: int, y: int]
        :param color: Tuple[b: int, g: int, r: int]
        :return: np.ndarray
        """

        x = pixel_coordinate[0]
        y = pixel_coordinate[1]

        size = MoilFisheyeMarker.__auto_point_size(image)
        thickness = MoilFisheyeMarker.__auto_thickness(image)
        if thickness == 0:
            thickness = 2

        cv2.line(image, (x, y - size), (x - size, y + size), color, thickness)
        cv2.line(image, (x, y - size), (x + size, y + size), color, thickness)
        cv2.line(image, (x + size, y + size), (x - size, y + size), color, thickness)

        return image

    @staticmethod
    def boundary_fov(image: np.ndarray,
                     moildev,
                     fov: int = 90,
                     color: tuple = (255, 255, 0)) -> np.ndarray:
        """
        Draw a field of view boundary oon the image.

        :param image: np.ndarray
        :param moildev: Moildev object
        :param fov: int
        :param color: Tuple[b: int, g: int, r: int]
        :return: np.ndarray
        """

        icx = moildev.icx
        icy = moildev.icy
        center = (icx, icy)

        boundary_radius = int(moildev.get_rho_from_alpha(fov))
        thickness = int(MoilFisheyeMarker.__auto_thickness(image) // 1.5)
        if thickness == 0:
            thickness = 2

        image = cv2.circle(image, center, radius=boundary_radius, color=color, thickness=thickness)

        return image

    @staticmethod
    def line_horizontal_vertical(image: np.ndarray,
                                 pixel_coordinate: Tuple[int, int],
                                 color: Tuple[int, int, int] = (0, 0, 0),
                                 translucent: float = 0.5):
        """
        Draw semi-transparent horizontal & vertical line at a certain coordinate on the image.

        :param image: np.ndarray
        :param pixel_coordinate: Tuple[x: int, y: int]
        :param color: Tuple[b: int, g: int, r: int]
        :param translucent: float (from 0.0 to 1.0)
        :return: np.ndarray
        """

        overlay = image.copy()
        translucent = 1 - translucent

        x, y = pixel_coordinate
        y_limit, x_limit = image.shape[:2]
        thickness = MoilFisheyeMarker.__auto_thickness(image)
        if thickness == 0:
            thickness = 2

        image = cv2.line(image, (0, y), (x_limit, y), color, thickness)
        image = cv2.line(image, (x, 0), (x, y_limit), color, thickness)

        result = cv2.addWeighted(overlay, translucent, image, 1 - translucent, 0)

        return result

    @staticmethod
    def line_p2p_distorted(image: np.ndarray,
                           moildev,
                           parameter_file: str,
                           start_img_point: tuple,
                           end_img_point: tuple,
                           color: Tuple[int, int, int] = (0, 0, 255)) -> np.ndarray:
        """
        Draw a distorted line between 2 point on the image.

        :param image: np.ndarray
        :param moildev: Moildev object
        :param parameter_file: str moil parameter file path
        :param start_img_point: Tuple[x: int, y: int]
        :param end_img_point: Tuple[x: int, y: int]
        :param color: Tuple[b: int, g: int, r: int]
        :return: np.ndarray
        """

        f = open(parameter_file)
        parameter = json.load(f)
        f.close()

        # Get the spherical coordinates of p1 and p2 vectors
        p1_theta = np.radians(moildev.get_alpha_beta(start_img_point[0], start_img_point[1])[0])
        p2_theta = np.radians(moildev.get_alpha_beta(end_img_point[0], end_img_point[1])[0])
        p1_phi = np.arctan2((-1) * start_img_point[1] + moildev.icy, start_img_point[0] - moildev.icx)
        p2_phi = np.arctan2((-1) * end_img_point[1] + moildev.icy, end_img_point[0] - moildev.icx)

        # Transform spherical coordinates into cartesian coordinates
        p1_v = MoilFisheyeMarker.__spherical2cartesian(p1_theta, p1_phi)
        p2_v = MoilFisheyeMarker.__spherical2cartesian(p2_theta, p2_phi)

        # Form a line from p1 to p2 in 3D space
        line_ps = np.linspace(0, 1, moildev.image_height + 1)
        line = p1_v + (p2_v - p1_v) * line_ps[:, None]

        # Convert cartesian coordinates into spherical coordinates
        line = MoilFisheyeMarker.__cartesian2spherical(line)

        # Convert the line in 3D space to img coordinate
        line = MoilFisheyeMarker.__space2img(line, moildev, parameter)

        # Round coordinate numbers to integers
        line = (np.rint(line)).astype(int)

        # Draw the line on the image
        radius = MoilFisheyeMarker.__auto_point_size(image) // 5
        for c in line:
            image = cv2.circle(image, (c[0], c[1]), radius=radius, color=color, thickness=-1)

        return image

    @staticmethod
    def __spherical2cartesian(theta: float, phi: float) -> np.ndarray:
        # convert a spherical coordinate (polar theta, azimuth phi) in radian of a vector to the cartesian one (x, y, z)
        return np.array([np.sin(theta) * np.cos(phi),
                         np.sin(theta) * np.sin(phi),
                         np.cos(theta)])

    @staticmethod
    def __cartesian2spherical(points: np.ndarray) -> np.ndarray:
        # convert cartesian coordinates (x, y, z) of vectors to spherical ones (theta, phi) in radian.
        points /= np.linalg.norm(points, axis=1)[:, None]
        sph = np.zeros((points.shape[0], 2))
        # compute theta
        sph[:, 0] = np.arccos(points[:, 2])
        # compute phi
        sph[:, 1] = np.arctan2(points[:, 1], points[:, 0])
        return sph

    @staticmethod
    def __space2img(points: np.ndarray,
                    moildev,
                    parameter: dict) -> np.ndarray:

        # Convert spherical coordinates of vectors in 3D space to image coordinates
        theta = points[:, 0]

        # get the distance of each point on the image to image center
        param_2 = moildev.param_2
        param_3 = moildev.param_3
        param_4 = moildev.param_4
        param_5 = moildev.param_5

        rho = (param_2 * theta ** 4 +
               param_3 * theta ** 3 +
               param_4 * theta ** 2 +
               param_5 * theta) * parameter['calibrationRatio']

        # compute x coordinates
        points[:, 0] = rho * np.cos(points[:, 1])
        # compute y coordinates
        points[:, 1] = rho * np.sin(points[:, 1])
        # adjust the origin of the coordinate system
        points = points + np.array([moildev.icx, -moildev.icy])
        # adjust y coordinates for the image coordinate system
        points[:, 1] = - points[:, 1]
        return points

