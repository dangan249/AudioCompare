from abc import ABCMeta
from abc import abstractmethod


class AbstractInputFile:
    """Defines the interface for input files."""
    __metaclass__= ABCMeta

    @abstractmethod
    def get_audio_samples(self, n):
        """Get n audio samples from each channel.
        Returns an array of arrays. There will be one
        array for each channel, each with n samples in it.
        If we encounter end of file, we may return less than
        n samples. If we were already at end of file, we raise
        EOFError."""
        pass

    @abstractmethod
    def get_channels(self):
        """Returns the number of channels in the file."""
        pass

    @abstractmethod
    def get_block_align(self):
        """Returns the number of bytes used in the file
        to represent a sample, multiplied by the number of channels."""
        pass

    @abstractmethod
    def get_sample_rate(self):
        """Returns the numbers of samples per second, per channel."""
        pass


    @abstractmethod
    def get_total_samples(self):
        """Returns the total number of samples per channel."""
        pass

    @abstractmethod
    def close(self):
        """Close the input file."""
        pass