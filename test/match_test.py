import sys
from WavInputFile import WavInputFile
import FFT
from Tkinter import *
import math


LOWER_LIMIT = 0
UPPER_LIMIT = 300
CHUNK_SIZE = 1024
RANGE = [40, 80, 120, 180, UPPER_LIMIT+1]

def get_bucket(freq):
    i = 0
    while RANGE[i] < freq:
        i += 1
    return i

def timestamp(chunk, chunk_size, samples_per_second):
    return float(chunk) * float(chunk_size) / float(samples_per_second)

def hash(file):
    try:
        input_file = WavInputFile(file)
    except IOError, e:
        print ("ERROR: {e}".format(e=e))
        return

    freq_chunks = FFT.FFT(input_file).series()

    chunks = len(freq_chunks)
    max = []
    max_index = []
    hashes = dict()
    for chunk in range(chunks):
        max.append([])
        max_index.append([])
        for freq in range(LOWER_LIMIT, UPPER_LIMIT):
            mag = math.log(math.fabs(freq_chunks[chunk][freq])+1)
            bucket = get_bucket(freq)
            if len(max[chunk]) <= bucket:
                max[chunk].append(mag)
                max_index[chunk].append(max_index)
            if mag > max[chunk][bucket]:
                max[chunk][bucket] = mag
                max_index[chunk][bucket] = freq
        time = timestamp(chunk, CHUNK_SIZE, input_file.get_sample_rate())
        #fuzz_factor = 2
        #hash = max[chunk][0]
        hash = "".join(["{:02.0f}".format(m) for m in max[chunk]])
        #print hash
        hashes[hash] = chunk

    #print len(hashes)
    #print len(hashes_unique)
    return hashes

def match_test():
    #hash1 = hash(sys.argv[1])
    #print "finished hash 1"
    hash2 = hash(sys.argv[2])
    print "finished hash 2"
    #database = [hash1, hash2]

    query_hash = hash(sys.argv[3])
    print "finished query hash"
    #print query_hash
    #print hash2.intersection(query_hash)
    diff = None
    for h in query_hash:
        #print h, query_hash[h]
        for h2 in hash2:
            if h == h2:
                if diff == None:
                    diff = (hash2[h2] - query_hash[h]) / 10
                elif ((hash2[h2] - query_hash[h]) / 10) == diff:
                    print "match at {c1},{c2}".format(c1=query_hash[h], c2=hash2[h2])



if __name__ == "__main__":
    match_test()