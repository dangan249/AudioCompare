from abc import ABCMeta
from abc import abstractmethod

class AbstractInputFile:
    __metaclass__= ABCMeta

    @abstractmethod
    def get_audio_samples(self, n):
        pass

    @abstractmethod
    def channels(self):
        pass

    @abstractmethod
    def block_align(self):
        pass