from FFT import FFT
import itertools
import numpy as np
from collections import defaultdict
from WavInputFile import WavInputFile

# This algorithm is based on the Shazam algorithm,
# described here http://www.redcode.nl/blog/2010/06/creating-shazam-in-java/
# and here http://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf

BUCKET_SIZE = 20
BUCKETS = 4
UPPER_LIMIT = (BUCKET_SIZE * BUCKETS)

CHUNK_SIZE = 1024

MAX_HASH_DISTANCE = 2
SCORE_THRESHOLD = 0


def _bucket_winners(freq_chunks):
    """Examine the results of running chunks of audio
    samples through FFT. For each chunk, look at the frequencies
    that are loudest in each "bucket." A bucket is a series of
    frequencies. Return the index of the loudest frequency in each
    bucket in each chunk."""
    chunks = len(freq_chunks)
    max_index = np.zeros((chunks, BUCKETS))
    # Examine each chunk independently
    for chunk in range(chunks):
        for bucket in range(BUCKETS):
            start_index = bucket * BUCKET_SIZE
            end_index = (bucket + 1) * BUCKET_SIZE
            bucket_vals = freq_chunks[chunk][start_index:end_index]
            raw_max_index = bucket_vals.argmax()
            max_index[chunk][bucket] = raw_max_index + start_index

    # return the indexes of the loudest frequencies
    return max_index


def _hash(max_index):
    """Turn the indexes of the loudest frequencies
    into a hash table. The frequency indices joined together
    into a tuple are the keys, and the chunk indices are
    the values. This means we can look up a sound fingerprint and find
    what time that sound happened in the audio recording."""
    hashes = defaultdict(list)
    for chunk in range(len(max_index)):
        hash = tuple(max_index[chunk])
        hashes[hash].append(chunk)

    return hashes


def _hash_distance(h1, h2):
    """The total difference between
    each number in two equal-length tuples."""
    if len(h1) != len(h2):
        raise ValueError("Arguments are sequences of unequal length")

    dist = 0
    for i in range(len(h1)):
        dist += abs(h1[i] - h2[i])

    return dist


def _file_fingerprint(filename):
    """Read the samples from the files, run them through FFT,
    find the loudest frequencies to use as fingerprints,
    turn those into a hash table."""
    result = [] 

    # Open the file
    file = WavInputFile(filename)

    # Read samples from the input files, divide them
    # into chunks by time, and convert the samples in each
    # chunk into the frequency domain.
    fft = FFT(file, CHUNK_SIZE).series()
    
    result.append( file.get_total_samples() / file.get_sample_rate() )

    file.close()

    # Find the indices of the loudest frequencies
    # in each "bucket" of frequencies (for every chunk).
    # These loud frequencies will become the
    # fingerprints that we'll use for matching.
    # Each chunk will be reduced to a tuple of
    # 4 numbers which are 4 of the loudest frequencies
    # in that chunk.
    winners = _bucket_winners(fft)

    # Generate a hash mapping the fingerprints
    # to the chunk numbers that they occurred in.
    # Chunk numbers are an approximation for the
    # timestamp in the file, and we'll use them
    # that way further on.

    result.append(_hash(winners) )

    return result # ugly solution !!!

class Wang:
    def __init__(self, filenames):
        self.filenames = filenames

    def match(self, debug=False):
        """Takes two AbstractInputFiles as input,
        and returns a boolean as output, indicating
        if the two files match."""

        # Get the fingerprints from each input file.
        # NOTE: @Charles: what if the 2 files are the same? (same location + same filename)
        # we can optimize further by avoid processing the same file twice
        result1, result2 = map(_file_fingerprint, self.filenames)
        
        hash1 = result1[1] # avoid modifying codes below
        hash2 = result2[1]

        # The difference in chunk numbers of
        # the matches we will find.
        # We'll map those differences to the number of matches
        # found with that difference.
        # This allows us to see if many fingerprints
        # from different files occurred at the same
        # time offsets relative to each other.
        offsets = defaultdict(lambda: 0)

        # Look to see if fingerprints from file 1
        # also were found in file 2. For matching
        # fingerprints, look up the the times (chunk number)
        # that the fingerprint occurred
        # in each file. Store the time differences in
        # offsets. The point of this is to see if there
        # are many matching fingerprints at the
        # same time difference relative to each
        # other. This indicates that the two files
        # contain similar audio.
        for h1 in hash1:
            if h1 in hash2:
                for c1, c2 in itertools.product(hash1[h1], hash2[h1]):
                    offset = c1 - c2
                    offsets[offset] += 1

        file1_len = result1[0]
        file2_len = result2[1]

        # The length of the shorter file in important
        # to deciding whether two audio files match.
        min_len = min(file1_len, file2_len)

        # max_offset is the highest number of times that two matching
        # hash keys were found with the same time difference
        # relative to each other.
        if len(offsets) != 0:
            max_offset = max(offsets.viewvalues())
        else:
            max_offset = 0

        # The score is the ratio of max_offset (as explained above)
        # to the length of the shorter file. A short file that should
        # match another file will result in less matching fingerprints
        # than a long file would, so we take this into account. At the
        # same time, a long file that should *not* match another file
        # will generate a decent number of matching fingerprints by
        # pure chance, so this corrects for that as well.
        score = max_offset / min_len

        # default behavior is to return boolean
        if not debug:
            if score > SCORE_THRESHOLD:
                return True
            else:
                return False

        # sometimes for debugging we return intermediate results
        return max_offset, min_len
