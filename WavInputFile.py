import chunk
import StringIO
import struct
from AbstractInputFile import AbstractInputFile

class WavInputFile(AbstractInputFile):

    def __init__(self, filename):
        wav_file = open(filename, "r")

        if not self.check_riff_format(wav_file):
            raise IOError("{f} is not a valid WAVE file".format(f=filename))
        wav_file.seek(0)

        riff_chunk = chunk.Chunk(wav_file, bigendian=False)
        riff_data = riff_chunk.read()

        if not self.check_wave_id(riff_data):
            raise IOError("{f} is not a valid WAVE file".format(f=filename))

        riff_data_io = StringIO.StringIO(riff_data[4:])

        if not self.check_fmt(riff_data_io):
            raise IOError("{f} is not a valid WAVE file".format(f=filename))
        riff_data_io.seek(0)

        fmt_chunk = chunk.Chunk(riff_data_io, bigendian=False)
        fmt_data = fmt_chunk.read()

        if not self.check_fmt_valid(fmt_data):
            raise IOError("{f} must be a valid WAVE_FORMAT_PCM file".format(f=filename))

        self.channels = self.read_short(fmt_data[2:4])

        self.block_align = self.read_short(fmt_data[12:14])

        self.data_chunk = chunk.Chunk(riff_data_io, bigendian=False)
        #self.audio_data = bytearray(data_chunk.read())

        wav_file.close()

    @staticmethod
    def check_riff_format(file):
        RIFF = file.read(4)
        if RIFF == "RIFF":
            return True
        else:
            return False

    @staticmethod
    def check_wave_id(data):
        WAVE = data[0:4]
        if WAVE == "WAVE":
            return True
        else:
            return False

    @staticmethod
    def check_fmt(file):
        fmt = file.read(4)
        size = WavInputFile.read_int(file.read(4))
        if fmt == "fmt " and size in [16, 18, 20]:
            return True
        else:
            return False

    @staticmethod
    def check_fmt_valid(data):
        format_tag = WavInputFile.read_short(data[0:2])
        if format_tag == 1:
            return True
        else:
            return False

    @staticmethod
    def read_short(data):
        return struct.unpack("<H", data)[0]

    @staticmethod
    def read_int(data):
        return struct.unpack("<I", data)[0]

    def get_audio_samples(self, n):
        bytes = self.block_align * n
        bbc = self.block_align / self.channels
        data = self.data_chunk.read(bytes)
        result = [[0]*n]*self.channels
        channel = 0
        sample = 0
        for i in range(0, bytes, self.block_align):
            result[channel][sample] = self.read_short(data[i:i+bbc])
            channel = channel % self.channels
            sample += 1

        return result

    def channels(self):
        return self.channels

    def block_align(self):
        return self.block_align
