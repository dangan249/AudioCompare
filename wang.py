from FFT import FFT
import math
import itertools
import numpy as np
from collections import defaultdict
import time

# This algorithm is based on the Shazam algorithm,
# described here http://www.redcode.nl/blog/2010/06/creating-shazam-in-java/
# and here http://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf

BUCKET_SIZE = 20
BUCKETS = 4
UPPER_LIMIT = (BUCKET_SIZE * BUCKETS)

CHUNK_SIZE = 1024

MAX_HASH_DISTANCE = 2


class Wang:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    @staticmethod
    def __get_bucket(freq_index):
        return freq_index / BUCKET_SIZE

    @staticmethod
    def __bucket_winners(freq_chunks):
        """Examine the results of running chunks of audio
        samples through FFT. For each chunk, look at the frequencies
        that are loudest in each "bucket." A bucket is a series of
        frequencies. Return the index of the loudest frequency in each
        bucket in each chunk."""
        chunks = len(freq_chunks)
        max = np.zeros((chunks, UPPER_LIMIT))
        max_index = np.zeros((chunks, UPPER_LIMIT))
        # Examine each chunk independently
        for chunk in range(chunks):
            # Look through some (or all) of the frequencies returned by FFT
            for freq in range(UPPER_LIMIT):
                # Compute the log of the magnitude of the audio at this
                # frequency.
                val = freq_chunks[chunk][freq]
                abs = math.sqrt((val.real * val.real) + (val.imag * val.imag)) + 1
                mag = math.log(abs)
                bucket = freq / BUCKET_SIZE
                # is this frequency louder than the previous loudest one
                # in this bucket?
                if mag > max[chunk][bucket]:
                    max[chunk][bucket] = mag
                    max_index[chunk][bucket] = freq

        # return the indexes of the loudest frequencies
        return max_index

    @staticmethod
    def __hash(max_index):
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

    @staticmethod
    def __hash_distance(h1, h2):
        """The total difference between
        each number in two equal-length tuples."""
        if len(h1) != len(h2):
            raise ValueError("Arguments are sequences of unequal length")

        dist = 0
        for i in range(len(h1)):
            dist += abs(h1[i] - h2[i])

        return dist

    def match(self):
        """Takes two AbstractInputFiles as input,
        and returns a boolean as output, indicating
        if the two files match."""

        start = time.time()

        # Read the samples from the files, run them through FFT,
        # find the loudest frequencies to use as fingerprints,
        # turn those into a hash table.

        # Read samples from the input files, divide them
        # into chunks, and convert the samples in each
        # chunk into the frequency domain
        fft1 = FFT(self.file1, CHUNK_SIZE).series(f=UPPER_LIMIT)
        fft2 = FFT(self.file2, CHUNK_SIZE).series(f=UPPER_LIMIT)

        #print "after FFT"
        #print time.time() - start

        # Find the indices of the loudest frequencies
        # in each "bucket" of frequencies (for every chunk)
        winners1 = Wang.__bucket_winners(fft1)
        winners2 = Wang.__bucket_winners(fft2)

       # print "after winners"
       # print time.time() - start

        # Generate a hash mapping the loudest frequency indices
        # to the chunk numbers
        hash1 = Wang.__hash(winners1)
        hash2 = Wang.__hash(winners2)

        #print "after hashes"
        #print time.time() - start

        # the difference in chunk numbers of
        # the matches we will find.
        # maps differences to number of matches
        # found with that difference
        offsets = defaultdict(lambda: 0)
        # compare every key in hash1 with every key
        # in hash 2
        #for h1, h2 in itertools.product(hash1, hash2):
            # if the two audio fingerprints are similar,
            # examine every place they occur
        #    if Wang.__hash_distance(h1, h2) < MAX_HASH_DISTANCE:
                # compare every chunk found for h1 with every
                # chunk found for h2
        #        for c1, c2 in itertools.product(hash1[h1], hash2[h2]):
        #            offset = c1 - c2
        #            offsets[offset] += 1

        for h1 in hash1:
            if h1 in hash2:
                for c1, c2 in itertools.product(hash1[h1], hash2[h1]):
                    offset = c1 - c2
                    offsets[offset] += 1

        #print "after lookups"
        #print time.time() - start

        # Let's assume that matching audio segments will only
        # generate 1 genuine "hit" for every 5 seconds of audio.
        # Whatever our shorter file is, the length of it in seconds
        # divided by 5 is the number of hits required to declare a
        # MATCH.
        #print max(offsets.viewvalues())
        #print sorted(offsets.values())
        file1_len = self.file1.get_total_samples() / self.file1.get_sample_rate()
        file2_len = self.file2.get_total_samples() / self.file2.get_sample_rate()
        threshold = 20 * min(file1_len, file2_len)

        #print "after threshold"
        #print time.time() - start

        if len(offsets) != 0 and max(offsets.viewvalues()) >= threshold:
            return True
        else:
            return False
