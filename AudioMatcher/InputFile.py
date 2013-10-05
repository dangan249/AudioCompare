from abc import ABCMeta

class InputFile:
    __metaclass__= ABCMeta

    @abstractmethod
    def get_audio_samples(self):
        pass

    @abstractmethod
    def channels(self):
        pass

    @abstractmethod
    def block_align(self):
        pass