#!/bin/env python

import sys
import chunk
import StringIO
import struct
from bitstring import BitArray

def read_short(data):
    return struct.unpack("<H", data)[0]
    
def read_int(data):
    return struct.unpack("<I", data)[0]
    
def write_int(data):
    return struct.pack("<I", data)

def encode_secret():
    if len(sys.argv) < 4:
        print ("Must provide args: input filename, ouput filename, secret string")
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
    
    j = 0
    i = 0
    secret_string = sys.argv[3]
    secret_bits = BitArray(bytes=secret_string)
    while j < len(secret_bits) and i < len(audio_data):
        lower_byte = audio_data[i + (bbc-1)]
        secret = secret_bits[j]
        if secret:
            lower_byte = lower_byte | 1
        else:
            lower_byte = lower_byte & ~(1)
        audio_data[i + (bbc-1)] = lower_byte
        
        j+=1
        i+=bbc
    
    # write the output file
    
    output_file = open(sys.argv[2], "w")
    output_file.write(riff_chunk.getname())
    output_file.write(write_int(riff_chunk.getsize()))
    output_file.write(riff_data[0:4])
    
    output_file.write(fmt_chunk.getname())
    output_file.write(write_int(fmt_chunk.getsize()))
    output_file.write(fmt_data)
    
    output_file.write(data_chunk.getname())
    output_file.write(write_int(data_chunk.getsize()))
    output_file.write(audio_data)
    
    output_file.close()


if __name__ == "__main__":
    encode_secret()
