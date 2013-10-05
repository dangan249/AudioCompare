
import InputFile
import chunk
import StringIO
import struct

class WavInputFile(InputFile):

    def __init__(self, filename):
        wav_file = open(filename, "r")

        if not self.check_file_format(wav_file):
            raise IOError("{f} is not a valid WAVE file".format(f=filename))

        riff_chunk = chunk.Chunk(wav_file, bigendian=False)
        riff_data = riff_chunk.read()
        riff_data_io = StringIO.StringIO(riff_data[4:])

        fmt_chunk = chunk.Chunk(riff_data_io, bigendian=False)
        fmt_data = fmt_chunk.read()

        format_tag = self.read_short(fmt_data[0:2])
        if format_tag != 1:
            print ("Must be a WAVE_FORMAT_PCM file")
            return

        self.channels = self.read_short(fmt_data[2:4])

        self.block_align = self.read_short(fmt_data[12:14])

        data_chunk = chunk.Chunk(riff_data_io, bigendian=False)
        self.audio_data = bytearray(data_chunk.read())

        wav_file.close()

    @staticmethod
    def check_riff_format(file):
        RIFF = file.read(4)
        file.read(4) # burn through 4 bytes to get to WAVE chunk
        WAVE = file.read(4)
        if RIFF == "RIFF" and WAVE == "WAVE":
            return True
        else:
            return False

    @staticmethod
    def read_short(data):
        return struct.unpack("<H", data)[0]

    def get_audio_samples(self):
        return self.audio_data