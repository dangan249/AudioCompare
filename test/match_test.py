import sys
from WavInputFile import WavInputFile
import FFT
import math
import numpy


BUCKET_SIZE = 20
LOWER_LIMIT = 1
BUCKETS = 4
UPPER_LIMIT = (BUCKET_SIZE * BUCKETS) + LOWER_LIMIT

def get_bucket(freq_index):
    return freq_index / BUCKET_SIZE

def timestamp(chunk, chunk_size, samples_per_second):
    return float(chunk) * float(chunk_size) / float(samples_per_second)

def bucket_winners(freq_chunks):
    # see fft_test for comments about this section
    chunks = len(freq_chunks)
    max = []
    max_index = []
    for chunk in range(chunks):
        max.append([])
        max_index.append([])
        for freq in range(LOWER_LIMIT, UPPER_LIMIT):
            val = freq_chunks[chunk][freq]
            abs = math.sqrt((val.real * val.real) + (val.imag * val.imag)) + 1
            mag = math.log(abs)
            bucket = freq / BUCKET_SIZE
            if len(max[chunk]) <= bucket:
                max[chunk].append(mag)
                max_index[chunk].append(freq)
            if mag > max[chunk][bucket]:
                max[chunk][bucket] = mag
                max_index[chunk][bucket] = freq

    return max_index

def fuzz(n, f):
    diff = n % f
    return n - diff

def hash(max_index):
    hashes = {}
    for chunk in range(len(max_index)):
        fuzz_factor = 2
        hash = "".join(["{:d} ".format(fuzz(max_index[chunk][m], fuzz_factor)) for m in range(BUCKETS)])
        hashes[hash] = chunk

    return hashes

def match_test():
    file1 = WavInputFile(sys.argv[1])
    hash1 = hash(bucket_winners(FFT.FFT(file1).series()))
    print "finished hash 1"

    file2 = WavInputFile(sys.argv[2])
    query_hash = hash(bucket_winners(FFT.FFT(file2).series()))
    print "finished query hash"

    diffs = {}
    for h in query_hash:
        for h1 in hash1:
            if h == h1:
                diff = (hash1[h1] - query_hash[h]) / 10
                if diff in diffs:
                    diffs[diff] += 1
                else:
                    diffs[diff] = 1

    print diffs

    for d in diffs:
        if diffs[d] >= 5:
            print "MATCH"
            return

    print "NO MATCH"


if __name__ == "__main__":
    match_test()