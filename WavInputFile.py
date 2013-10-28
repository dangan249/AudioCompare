import struct
import numpy as np
import tempfile
import shutil
import subprocess 
import os

from AbstractInputFile import AbstractInputFile


class WavInputFile(AbstractInputFile):

    def __init__(self, filename):
        """Open a WAVE file with the given file path.
        This document http://www-mmsp.ece.mcgill.ca/documents/AudioFormats/WAVE/WAVE.html
        was used as a spec for files. We implement a limited subset
        of the WAVE format. We assume a RIFF chunk contains a fmt
        chunk and then a data chunk, and do not read past that.
        We also will only open WAVE_FORMAT_PCM files.

        At the end of this constructor. self.wav_file will be positioned
        at the first byte of audio data in the file."""


        self.workingdir = tempfile.mkdtemp()
        wavfilespec = self.workingdir + "/tempwavfile.wav"

        print "************DEBUG************"
        print "\n"
        print wavfilespec
        print "\n"
        print "************DEBUG************"

        # Use lame to make a wav representation of the mp3 file to be analyzed
        lame = '/course/cs4500f13/bin/lame --decode %s %s' % (filename, canonical_form)
        subprocess.call([lame], shell=True, stderr=open(os.devnull, 'w'))

        self.wav_file = open( canonical_form , "r")

        # check for RIFF in beginning of file
        if not self.__check_riff_format(self.wav_file):
            raise IOError("{f} is not a valid WAVE file".format(f=filename))
        riff_size = WavInputFile.__read_size(self.wav_file)

        # Check for WAVE
        if not self.__check_wave_id(self.wav_file):
            raise IOError("{f} is not a valid WAVE file".format(f=filename))

        #riff_data_io = cStringIO.StringIO(riff_data[4:])

        # check that we just opened a fmt chunk
        if not self.__check_fmt(self.wav_file):
            raise IOError("{f} is not a valid WAVE file".format(f=filename))
        fmt_chunk_size = WavInputFile.__read_size(self.wav_file)

        fmt_data = self.wav_file.read(fmt_chunk_size)

        # We only handle PCM files
        if not self.__check_fmt_valid(fmt_data):
            raise IOError("{f} must be a valid WAVE_FORMAT_PCM file".format(f=filename))

        # get some info from the file header
        self.channels = self.__read_ushort(fmt_data[2:4])
        self.sample_rate = self.__read_uint(fmt_data[4:8])
        self.block_align = self.__read_ushort(fmt_data[12:14])

        if not self.__check_data(self.wav_file):
            raise IOError("{f} is not a valid WAVE file".format(f=filename))

        self.data_chunk_size = WavInputFile.__read_size(self.wav_file)
        self.total_samples = (self.data_chunk_size / self.block_align)

    @staticmethod
    def __check_riff_format(file):
        RIFF = file.read(4)
        return RIFF == "RIFF"

    @staticmethod
    def __check_wave_id(file):
        WAVE = file.read(4)
        return WAVE == "WAVE"

    @staticmethod
    def __check_fmt(file):
        fmt = file.read(4)
        return fmt == "fmt "

    @staticmethod
    def __check_data(file):
        data = file.read(4)
        return data == "data"

    @staticmethod
    def __check_fmt_valid(data):
        format_tag = WavInputFile.__read_ushort(data[0:2])
        return format_tag == 1

    @staticmethod
    def __read_size(file):
        """Read a 4 byte uint from the file."""
        return WavInputFile.__read_uint(file.read(4))

    @staticmethod
    def __read_ushort(data):
        """Turn a 2-byte little endian number into a Python number."""
        return struct.unpack("<H", data)[0]

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
        EOFError.

        This function assumes that self.wav_file is positioned
        at the place in the file you want to read from."""
        data = np.fromfile(self.wav_file, dtype=np.int16, count=n*self.channels)
        result = np.zeros((self.channels, n), dtype=int)
        for c in range(self.channels):
            result[c] = data[c::self.channels]

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
        self.wav_file.close()
        #Delete temporary working directory and its contents.
        shutil.rmtree(self.workingdir)
    

