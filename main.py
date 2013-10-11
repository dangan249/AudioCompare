import sys
from WavInputFile import WavInputFile
from FFT import FFT
import math

# This algorithm is based on the Shazam algorithm,
# described here http://www.redcode.nl/blog/2010/06/creating-shazam-in-java/
# and here http://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf

BUCKET_SIZE = 20
LOWER_LIMIT = 1
BUCKETS = 4
UPPER_LIMIT = (BUCKET_SIZE * BUCKETS) + LOWER_LIMIT

def get_bucket(freq_index):
    return freq_index / BUCKET_SIZE

def fuzz(n, f):
    diff = n % f
    return n - diff

def bucket_winners(freq_chunks):
    """Examine the results of running chunks of audio
    samples through FFT. For each chunk, look at the frequencies
    that are loudest in each "bucket." A bucket is a series of
    frequencies. Return the index of the loudest frequency in each
    bucket in each chunk."""
    # see fft_test for comments about this section
    chunks = len(freq_chunks)
    max = []
    max_index = []
    # Examine each chunk independently
    for chunk in range(chunks):
        max.append([])
        max_index.append([])
        # Look through some (or all) of the frequencies returned by FFT
        for freq in range(LOWER_LIMIT, UPPER_LIMIT):
            # Compute the log of the magnitude of the audio at this
            # frequency.
            val = freq_chunks[chunk][freq]
            abs = math.sqrt((val.real * val.real) + (val.imag * val.imag)) + 1
            mag = math.log(abs)
            bucket = freq / BUCKET_SIZE
            # If we haven't looked at this bucket yet,
            # this frequency is definitely the loudest one
            # in this bucket
            if len(max[chunk]) <= bucket:
                max[chunk].append(mag)
                max_index[chunk].append(freq)
            # is this frequency louder than the previous loudest one
            # in this bucket?
            if mag > max[chunk][bucket]:
                max[chunk][bucket] = mag
                max_index[chunk][bucket] = freq

    # return the indexes of the loudest frequencies
    return max_index

def hash(max_index):
    """Turn the indexes of the loudest frequencies
    into a hash table. The frequency indices joined together
    into a string are the keys, and the chunk indices are
    the keys. This means we can look up a sound fingerprint and find
    what time that sound happened in the audio recording."""
    hashes = {}
    for chunk in range(len(max_index)):
        fuzz_factor = 2
        hash = "".join(["{:d} ".format(fuzz(max_index[chunk][m], fuzz_factor)) for m in range(BUCKETS)])
        hashes[hash] = chunk

    return hashes

def audio_matcher():
    """Our main control flow."""
    if len(sys.argv) < 3:
        print "Must provide two input files."
        return

    # Open the two input files
    try:
        file1 = WavInputFile(sys.argv[1])
        file2 = WavInputFile(sys.argv[2])
    except IOError, e:
        print ("ERROR: {e}".format(e=e))
        return

    # Read the samples from the files, run them through FFT,
    # find the loudest frequencies to use as fingerprints,
    # turn those into a hash table.
    hash1 = hash(bucket_winners(FFT(file1).series()))
    hash2 = hash(bucket_winners(FFT(file2).series()))

    # the difference in chunk numbers of
    # the matches we will find.
    # maps differences to number of matches
    # found with that difference
    diffs = {}
    # compare every key in hash1 with every key
    # in hash 2
    for h2 in hash2:
        for h1 in hash1:
            # if the keys match
            if h2 == h1:
                # find the difference in their chunk numbers
                # and note that we found one more match
                # at with this chunk difference
                diff = (hash1[h1] - hash2[h2]) / 10
                if diff in diffs:
                    diffs[diff] += 1
                else:
                    diffs[diff] = 1

    # if any matches occurred at the same time difference
    # more than 5 times, we'll say the two files match
    # this is a stupid heuristic that will need to be improved
    for d in diffs:
        if diffs[d] >= 5:
            print "MATCH"
            return

    print "NO MATCH"

if __name__ == "__main__":
    audio_matcher()