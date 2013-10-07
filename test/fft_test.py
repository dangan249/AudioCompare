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
    try:
        input_file = WavInputFile(sys.argv[1])
    except IOError, e:
        print ("ERROR: {e}".format(e=e))
        return

    #dsp = ossaudiodev.open('/dev/dsp', 'w')
    #dsp.setparameters(ossaudiodev.AFMT_S16_LE, input_file.get_channels(), input_file.get_sample_rate())
    #while True:
    #    samples = input_file.get_audio_samples(1024)
    #    bytes = ""
    #    channel = 0
    #    for i in range(1024):
    #        bytes += write_short(samples[channel][i])
    #        channel = channel * input_file.get_channels()
        #print len(bytes)
    #    if len(bytes) == 0:
    #        return
    #    dsp.write(bytes)
    #return


    fft = FFT.FFT(input_file, CHUNK_SIZE)
    freq_chunks = fft.series()
    #for f in freq_chunks:
    #    print f[0]
    print len(freq_chunks)
    base_freq = fft.base_freq()

    max = []
    max_index = []
    for chunk in range(len(freq_chunks)):
        max.append({})
        max_index.append({})
        #print chunk
        for freq in range(LOWER_LIMIT, UPPER_LIMIT):
            mag = math.log(math.fabs(freq_chunks[chunk][freq])+1)
            #mag_array.append(mag)
            bucket = get_bucket(freq)
            if not bucket in max[chunk]:
                max[chunk][bucket] = mag
                max_index[chunk][bucket] = freq
            if mag > max[chunk][bucket]:
                max[chunk][bucket] = mag
                max_index[chunk][bucket] = freq
        #print mag_array


    for r in max_index:
        print r

def get_bucket(freq):
    i = 0
    while RANGE[i] < freq:
        i += 1
    return i

if __name__ == "__main__":
    fft_test()