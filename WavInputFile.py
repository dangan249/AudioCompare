import struct
import numpy as np
import tempfile
import shutil
import subprocess 
import os
import time

from AbstractInputFile import AbstractInputFile


class WavInputFile(AbstractInputFile):

    def __init__(self, filename):
        """Open an Audio file with the given file path.
        Supported formats: WAVE, MP3.
        All MP3 files will be converted to WAVE using the LAME programe

        This document http://www-mmsp.ece.mcgill.ca/documents/AudioFormats/WAVE/WAVE.html
        was used as a spec for files. We implement a limited subset
        of the WAVE format. We assume a RIFF chunk contains a fmt
        chunk and then a data chunk, and do not read past that.
        We also will only open WAVE_FORMAT_PCM files.

        At the end of this constructor. self.wav_file will be positioned
        at the first byte of audio data in the file."""
        
        self.wav_file = open( filename, "r" )
        #try to use lame to convert
        self.workingdir = tempfile.mkdtemp()

        if  not self.__is_wave_file( self.wav_file ):   
            self.wav_file.close()
            canonical_form = self.workingdir + "/tempwavfile" + str( time.time() )
            # Use lame to make a wav representation of the mp3 file to be analyzed
            lame = '/course/cs4500f13/bin/lame --silent --decode %s %s' % (filename, canonical_form)
            return_code = subprocess.call([lame], shell=True)                
            
            if return_code != 0 or not os.path.exists(canonical_form):
                raise IOError("{f} 's format is not supported".format(f=filename))
            
            # At this point, we should be confident that "lame" create a correct WAVE file
            self.wav_file = open( canonical_form , "r")
            
       # At this point, audio file should have the canonical form(WAVE)    
        self.wav_file.seek(4,0)
        riff_size = WavInputFile.__read_size(self.wav_file)

        self.wav_file.seek(16,0)
        fmt_chunk_size = WavInputFile.__read_size(self.wav_file)
        fmt_data = self.wav_file.read(fmt_chunk_size)
        
        # get some info from the file header
        self.channels = self.__read_ushort(fmt_data[2:4])
        self.sample_rate = self.__read_uint(fmt_data[4:8])
        self.block_align = self.__read_ushort(fmt_data[12:14])

        self.wav_file.seek( 40 , 0 )
        self.data_chunk_size = WavInputFile.__read_size(self.wav_file)
        self.total_samples = (self.data_chunk_size / self.block_align)

    @staticmethod
    def __is_wave_file(file):
        if( WavInputFile.__check_riff_format(file) 
            and WavInputFile.__check_wave_id(file)
            and WavInputFile.__check_fmt(file) ):            
            file.seek( 20 )
            data = file.read( 2 ) 
            file.seek( 0 )
            return ( WavInputFile.__check_fmt_valid(data) 
                     and WavInputFile.__check_data(file) )
        else:
            return False

    @staticmethod
    def __check_riff_format(file):
        RIFF = file.read(4)
        file.seek(0)
        return RIFF == "RIFF"

    @staticmethod
    def __check_wave_id(file):
        file.seek(8)
        WAVE = file.read(4)
        file.seek(0)
        return WAVE == "WAVE"

    @staticmethod
    def __check_fmt(file):
        file.seek(12)
        fmt = file.read(4)
        file.seek(0)
        return fmt == "fmt "

    @staticmethod
    def __check_data(file):
        file.seek(36)
        data = file.read(4)
        file.seek(0)
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
    

