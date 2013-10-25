from FFT import FFT
import itertools
import numpy as np
from collections import defaultdict
import multiprocessing
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

    # Open the file
    file = WavInputFile(filename)

    # Read samples from the input files, divide them
    # into chunks, and convert the samples in each
    # chunk into the frequency domain
    fft = FFT(file, CHUNK_SIZE).series()

    # Find the indices of the loudest frequencies
    # in each "bucket" of frequencies (for every chunk)
    winners = _bucket_winners(fft)

    # Generate a hash mapping the loudest frequency indices
    # to the chunk numbers
    return _hash(winners)

class Wang:
    def __init__(self, filenames):
        self.filenames = filenames

    def match(self, debug=False):
        """Takes two AbstractInputFiles as input,
        and returns a boolean as output, indicating
        if the two files match."""

        try:
            num_processes = multiprocessing.cpu_count()
        except NotImplementedError:
            num_processes = 2
        #pool = multiprocessing.Pool(processes=num_processes)

        #hash1, hash2 = pool.map(_file_fingerprint, self.filenames)
        hash1, hash2 = map(_file_fingerprint, self.filenames)

        # the difference in chunk numbers of
        # the matches we will find.
        # maps differences to number of matches
        # found with that difference
        offsets = defaultdict(lambda: 0)

        for h1 in hash1:
            if h1 in hash2:
                for c1, c2 in itertools.product(hash1[h1], hash2[h1]):
                    offset = c1 - c2
                    offsets[offset] += 1

        #for h1, h2 in itertools.product(hash1, hash2):
        #    if _hash_distance(h1, h2) < MAX_HASH_DISTANCE:
        #        for c1, c2 in itertools.product(hash1[h1], hash2[h1]):
        #            offset = c1 - c2
        #            offsets[offset] += 1

        # Let's assume that matching audio segments will only
        # generate 1 genuine "hit" for every 5 seconds of audio.
        # Whatever our shorter file is, the length of it in seconds
        # divided by 5 is the number of hits required to declare a
        # MATCH.
        #print max(offsets.viewvalues())
        #print sorted(offsets.values())
        file1 = WavInputFile(self.filenames[0])
        file2 = WavInputFile(self.filenames[1])
        file1_len = file1.get_total_samples() / file1.get_sample_rate()
        file2_len = file2.get_total_samples() / file2.get_sample_rate()

        min_len = min(file1_len, file2_len)

        if len(offsets) != 0:
            max_offset = max(offsets.viewvalues())
        else:
            max_offset = 0

        score = max_offset / min_len

        # default behavior is to return boolean
        if not debug:
            if score > SCORE_THRESHOLD:
                return True
            else:
                return False

        # sometimes for debugging we return intermediate results
        return max_offset, min_len