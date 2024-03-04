from abc import ABC, abstractmethod
from typing import Tuple, List

import numpy as np


class AbstractMoilCamera(ABC):

    @classmethod
    def scan(cls) -> List[int] or List[str]:
        """
        List valid camera ID

        :return: list
        """
        pass

    @abstractmethod
    def open(self) -> bool:
        """
        Open camera by camera ID

        :return: bool
        """
        pass

    @abstractmethod
    def frame(self) -> np.ndarray:
        """
        Get single frame

        :return: numpy.ndarray
        """
        pass

    @abstractmethod
    def close(self) -> bool:
        """
        Close camera

        :return: bool
        """
        pass

    @abstractmethod
    def is_open(self) -> bool:
        """
        Is camera open ?

        :return: bool
        """
        pass

    @abstractmethod
    def get_resolution(self) -> Tuple[int, int]:
        """
        Return current resolution

        :return: Tuple[width: int, height: int]
        """
        pass

    @abstractmethod
    def set_resolution(self, resolution: Tuple[int, int]) -> Tuple[int, int]:
        """
        Set current resolution

        :return: Tuple[width: int, height: int] or warning_msg: str
        """
        pass
