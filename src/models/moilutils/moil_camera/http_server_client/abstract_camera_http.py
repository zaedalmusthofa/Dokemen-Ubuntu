import abc


class AbstractCameraModule(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def single_image(self):
        pass
