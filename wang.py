from FFT import FFT
import math
import itertools

# This algorithm is based on the Shazam algorithm,
# described here http://www.redcode.nl/blog/2010/06/creating-shazam-in-java/
# and here http://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf

BUCKET_SIZE = 20
LOWER_LIMIT = 1
BUCKETS = 4
UPPER_LIMIT = (BUCKET_SIZE * BUCKETS) + LOWER_LIMIT

CHUNK_SIZE = 8196

MAX_HASH_DISTANCE = 2

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
        hash = tuple(max_index[chunk])
        if hash in hashes:
            hashes[hash].append(chunk)
        else:
            hashes[hash] = [chunk]

    return hashes

def hash_distance(h1, h2):
    if len(h1) != len(h2):
        raise ValueError("Arguments are sequences of unequal length")

    dist = 0
    for i in range(len(h1)):
        dist += abs(h1[i] - h2[i])

    return dist

def matcher(file1, file2):

    # Read the samples from the files, run them through FFT,
    # find the loudest frequencies to use as fingerprints,
    # turn those into a hash table.
    hash1 = hash(bucket_winners(FFT(file1, CHUNK_SIZE).series()))
    hash2 = hash(bucket_winners(FFT(file2, CHUNK_SIZE).series()))

    # the difference in chunk numbers of
    # the matches we will find.
    # maps differences to number of matches
    # found with that difference
    offsets = {}
    # compare every key in hash1 with every key
    # in hash 2
    for h1, h2 in itertools.product(hash1, hash2):
        if hash_distance(h1, h2) < MAX_HASH_DISTANCE:
            for c1, c2 in itertools.product(hash1[h1], hash2[h2]):
                offset = c1 - c2
                if offset in offsets:
                    offsets[offset] += 1
                else:
                    offsets[offset] = 1

    # if any matches occurred at the same time difference
    # more than 5 times, we'll say the two files match
    # this is a stupid heuristic that will need to be improved
    #print max(offsets.viewvalues())
    if len(offsets) != 0 and max(offsets.viewvalues()) >= 5:
        return True
    else:
        return False
