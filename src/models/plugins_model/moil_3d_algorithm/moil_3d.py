from typing import Tuple
import numpy as np


class Moil3dAlgorithm:

    @staticmethod
    def __moil2cartesian(alpha: float, beta: float) -> np.ndarray:
        # convert a moildev coordinate (alpha, beta) in radian of a vector to the cartesian one (x, y, z)
        return np.array([np.sin(alpha) * np.sin(beta),
                         np.sin(alpha) * np.cos(beta),
                         np.cos(alpha)])

    @staticmethod
    def __rotate_3d_vector_about_y_axis(rotate_deg: float, vector) -> np.ndarray:
        r_matrix = np.array([[np.cos(np.radians(rotate_deg)), 0, np.sin(np.radians(rotate_deg))],
                             [0, 1, 0],
                             [-np.sin(np.radians(rotate_deg)), 0, np.cos(np.radians(rotate_deg))]])

        return r_matrix.dot(vector)

    @staticmethod
    def __get_nearest_point(l_p_vector, r_p_vector, camera_distance) -> np.ndarray:
        eqns = np.array([[l_p_vector[0] ** 2, -l_p_vector[0] * r_p_vector[0]],
                         [l_p_vector[2] ** 2, -l_p_vector[2] * r_p_vector[2]]])
        p_n = np.array([camera_distance * l_p_vector[0], 0])
        p_solve = np.linalg.solve(eqns, p_n)
        return 0.5 * (p_solve[0] * l_p_vector + p_solve[1] * r_p_vector + np.array([camera_distance, 0, 0]))

    @staticmethod
    def measure_3d_distance(cam1_moildev, cam2_moildev,
                            cam1_p1: Tuple, cam1_p2: Tuple, cam2_p1: Tuple, cam2_p2: Tuple,
                            camera_distance: float = 0, face2face: bool = False) -> float:
        """
        :param cam1_moildev: Moildev object (cam_1)
        :param cam2_moildev: Moildev object (cam_2)
        :param cam1_p1: Tuple[x: int, y: int] pixel coord "p1" (cam_1)
        :param cam1_p2: Tuple[x: int, y: int] pixel coord "p2" (cam_1)
        :param cam2_p1: Tuple[x: int, y: int] pixel coord "p1" (cam_2)
        :param cam2_p2: Tuple[x: int, y: int] pixel coord "p2" (cam_2)
        :param camera_distance: float (Distance between cam_1 & cam_2)
        :param face2face: bool (Is cam_1 & cam_2 face to face)
        :return: float
        """
        """
        The coordinate system rotation doesn't work in quick_3d_measure(Adam algorithm),
        so Ada provided my solution for 3D measurement. by Ada
        """
        # get alpha and beta of points from Moildev, and convert them into radians
        l_p1 = np.radians(cam1_moildev.get_alpha_beta(*cam1_p1))
        l_p2 = np.radians(cam1_moildev.get_alpha_beta(*cam1_p2))
        r_p1 = np.radians(cam2_moildev.get_alpha_beta(*cam2_p1))
        r_p2 = np.radians(cam2_moildev.get_alpha_beta(*cam2_p2))

        # convert moildev coordinates (alpha, beta) to cartesian (x, y, z)
        l_p1_v = Moil3dAlgorithm.__moil2cartesian(*l_p1)
        l_p2_v = Moil3dAlgorithm.__moil2cartesian(*l_p2)
        r_p1_v = Moil3dAlgorithm.__moil2cartesian(*r_p1)
        r_p2_v = Moil3dAlgorithm.__moil2cartesian(*r_p2)

        # if the cameras are face to face, rotate both coordinate systems for 90 degrees about the y-axis
        if face2face:
            l_p1_v = Moil3dAlgorithm.__rotate_3d_vector_about_y_axis(90, l_p1_v)
            l_p2_v = Moil3dAlgorithm.__rotate_3d_vector_about_y_axis(90, l_p2_v)
            r_p1_v = Moil3dAlgorithm.__rotate_3d_vector_about_y_axis(-90, r_p1_v)
            r_p2_v = Moil3dAlgorithm.__rotate_3d_vector_about_y_axis(-90, r_p2_v)

        # Get p1 and p2
        final_p1 = Moil3dAlgorithm.__get_nearest_point(l_p1_v, r_p1_v, camera_distance)
        final_p2 = Moil3dAlgorithm.__get_nearest_point(l_p2_v, r_p2_v, camera_distance)

        return np.round(np.linalg.norm(final_p1 - final_p2), 2)
