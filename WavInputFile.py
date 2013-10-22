import chunk
import StringIO
import struct
import numpy as np
from AbstractInputFile import AbstractInputFile


class WavInputFile(AbstractInputFile):

    def __init__(self, filename):
        """Open a WAVE file with the given file path.
        This document http://www-mmsp.ece.mcgill.ca/documents/AudioFormats/WAVE/WAVE.html
        was used as a spec for files. We implement a limited subset
        of the WAVE format. We assume a RIFF chunk contains a fmt
        chunk and then a data chunk, and do not read past that.
        We also will only open WAVE_FORMAT_PCM files."""
        self.wav_file = open(filename, "r")

        # check for RIFF in beginning of file
        if not self.__check_riff_format(self.wav_file):
            raise IOError("{f} is not a valid WAVE file".format(f=filename))
        self.wav_file.seek(0)

        # Open outer RIFF chunk
        riff_chunk = chunk.Chunk(self.wav_file, bigendian=False)
        riff_data = riff_chunk.read()

        # Check for WAVE
        if not self.__check_wave_id(riff_data):
            raise IOError("{f} is not a valid WAVE file".format(f=filename))

        riff_data_io = StringIO.StringIO(riff_data[4:])

        # check that we just opened a fmt chunk
        if not self.__check_fmt(riff_data_io):
            raise IOError("{f} is not a valid WAVE file".format(f=filename))
        riff_data_io.seek(0)

        fmt_chunk = chunk.Chunk(riff_data_io, bigendian=False)
        fmt_data = fmt_chunk.read()

        # We only handle PCM files
        if not self.__check_fmt_valid(fmt_data):
            raise IOError("{f} must be a valid WAVE_FORMAT_PCM file".format(f=filename))

        # get some info from the file header
        self.channels = self.__read_ushort(fmt_data[2:4])
        self.sample_rate = self.__read_uint(fmt_data[4:8])
        self.block_align = self.__read_ushort(fmt_data[12:14])

        self.data_chunk = chunk.Chunk(riff_data_io, bigendian=False)
        self.total_samples = (self.data_chunk.getsize() / self.block_align)

    @staticmethod
    def __check_riff_format(file):
        RIFF = file.read(4)
        if RIFF == "RIFF":
            return True
        else:
            return False

    @staticmethod
    def __check_wave_id(data):
        WAVE = data[0:4]
        if WAVE == "WAVE":
            return True
        else:
            return False

    @staticmethod
    def __check_fmt(file):
        fmt = file.read(4)
        size = WavInputFile.__read_uint(file.read(4))
        if fmt == "fmt " and size in [16, 18, 20]:
            return True
        else:
            return False

    @staticmethod
    def __check_fmt_valid(data):
        format_tag = WavInputFile.__read_ushort(data[0:2])
        if format_tag == 1:
            return True
        else:
            return False

    @staticmethod
    def __read_ushort(data):
        """Turn a 2-byte little endian number into a Python number."""
        return struct.unpack("<H", data)[0]

    @staticmethod
    def __read_short(data):
        """Turn a 2-byte little endian number into a Python number."""
        return struct.unpack("<h", data)[0]

    @staticmethod
    def __read_uint(data):
        """Turn a 4-byte little endian number into a Python number."""
        return struct.unpack("<I", data)[0]

    def get_audio_samples(self, n):
        """Get n audio samples from each channel.
        Returns an array of arrays. There will be one
        array for each channel, each with n samples in it.
        If we encounter end of file, we may return less than
        n samples. If we were already at end of file, we raise
        EOFError."""
        bytes = self.block_align * n
        bbc = self.block_align / self.channels
        data = self.data_chunk.read(bytes)
        if len(data) == 0:
            raise EOFError
        result = np.zeros((self.channels, n), dtype=int)
        channel = 0
        sample = 0
        for i in range(0, len(data), self.block_align):
            result[channel][sample] = WavInputFile.__read_short(data[i:i+bbc])
            channel = channel % self.channels
            sample += 1

        return result

    def get_channels(self):
        """Returns the number of channels in the file."""
        return self.channels

    def get_block_align(self):
        """Returns the number of bytes used in the file
        to represent a sample, multiplied by the number of channels."""
        return self.block_align

    def get_sample_rate(self):
        """Returns the numbers of samples per second, per channel."""
        return self.sample_rate

    def get_total_samples(self):
        """Returns the total number of samples per channel."""
        return self.total_samples

    def close(self):
        """Close the input file."""
        self.data_chunk.close()
        self.wav_file.close()