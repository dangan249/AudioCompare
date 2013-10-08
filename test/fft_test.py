import sys
from WavInputFile import WavInputFile
import FFT
import math
import ossaudiodev
import struct


LOWER_LIMIT = 0
UPPER_LIMIT = 300
CHUNK_SIZE = 4096
RANGE = [40, 80, 120, 180, UPPER_LIMIT+1]

def write_short(data):
    return struct.pack("<H", data)

def fft_test():
    # open an input file
    try:
        input_file = WavInputFile(sys.argv[1])
    except IOError, e:
        print ("ERROR: {e}".format(e=e))
        return

    # Compute FFT of each chunk of the file
    fft = FFT.FFT(input_file, CHUNK_SIZE)
    freq_chunks = fft.series()
    print len(freq_chunks)

    max = []
    max_index = []
    # examine each chunk in the file separately
    for chunk in range(len(freq_chunks)):
        max.append({})
        max_index.append({})
        # examine each frequency, and see if that frequency
        # is the loudest in its "bucket"
        # a bucket is a range of frequencies
        for freq in range(LOWER_LIMIT, UPPER_LIMIT):
            mag = math.log(math.fabs(freq_chunks[chunk][freq])+1)
            bucket = get_bucket(freq)
            if not bucket in max[chunk]:
                max[chunk][bucket] = mag
                max_index[chunk][bucket] = freq
            if mag > max[chunk][bucket]:
                max[chunk][bucket] = mag
                max_index[chunk][bucket] = freq

def get_bucket(freq):
    i = 0
    while RANGE[i] < freq:
        i += 1
    return i

if __name__ == "__main__":
    fft_test()