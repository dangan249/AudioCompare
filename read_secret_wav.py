#!/bin/env python

import sys
import chunk
import StringIO
import struct
from bitstring import BitArray, Bits

def read_short(data):
    return struct.unpack("<H", data)[0]
    
def read_int(data):
    return struct.unpack("<I", data)[0]

def read_secret():
    if len(sys.argv) < 2:
        print ("Must provide input filename")
        return
        
    # open the input file
    wav_file = open(sys.argv[1], "r")
    riff_chunk = chunk.Chunk(wav_file, bigendian=False)
    riff_data = riff_chunk.read()
    riff_data_io = StringIO.StringIO(riff_data[4:])
    
    fmt_chunk = chunk.Chunk(riff_data_io, bigendian=False)
    fmt_data = fmt_chunk.read()
    
    format_tag = read_short(fmt_data[0:2])
    if format_tag != 1:
        print ("Must be a WAVE_FORMAT_PCM file")
        return
        
    channels = read_short(fmt_data[2:4])
    
    block_align = read_short(fmt_data[12:14])
    
    data_chunk = chunk.Chunk(riff_data_io, bigendian=False)
    audio_data = bytearray(data_chunk.read())
    
    wav_file.close()
        
    bbc = block_align / channels
    
    i = 0
    j = 0
    secret_bits = BitArray()
    true_bit = Bits("0b1")
    false_bit = Bits("0b0")
    while i+1 < len(audio_data):
        lower_byte = audio_data[i + 1]
        secret = lower_byte & 1
        if secret == 1:
            secret_bits += true_bit
        else:
            secret_bits += false_bit
        
        if (i % 100000) == 0:
            sys.stderr.write ("progress: {p}%\n".format(p= 100 * i / float(len(audio_data))))
        
        j+=1
        i+=bbc
    
    print (secret_bits.tobytes())
    

if __name__ == "__main__":
    read_secret()
