from abc import ABCMeta
from abc import abstractmethod

class AbstractInputFile:
    __metaclass__= ABCMeta

    @abstractmethod
    def get_audio_samples(self, n):
        pass

    @abstractmethod
    def get_channels(self):
        pass

    @abstractmethod
    def get_block_align(self):
        pass

    @abstractmethod
    def get_sample_rate(self):
        pass


    @abstractmethod
    def get_total_samples(self):
        pass

    @abstractmethod
    def close(self):
        pass