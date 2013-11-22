import math
import time
from FFT import FFT
import numpy as np
from collections import defaultdict
from InputFile import InputFile
import multiprocessing
import os
import stat
from error import *

# This algorithm is based on the Shazam algorithm,
# described here http://www.redcode.nl/blog/2010/06/creating-shazam-in-java/
# and here http://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf

BUCKET_SIZE = 20
BUCKETS = 4
UPPER_LIMIT = (BUCKET_SIZE * BUCKETS)
BITS_PER_NUMBER = int(math.ceil(math.log(BUCKET_SIZE, 2)))
assert((BITS_PER_NUMBER * BUCKETS) <= 32)

NORMAL_CHUNK_SIZE = 1024
NORMAL_SAMPLE_RATE = 44100.0

MAX_HASH_DISTANCE = 2
SCORE_THRESHOLD = 0


class FileResult:
    """The result of fingerprinting
    an entire audio file."""
    def __init__(self, fingerprints, file_len, filename):
        self.fingerprints = fingerprints
        self.file_len = file_len
        self.filename = filename

    def __str__(self):
        return self.filename


class ChunkInfo:
    """These objects will be the values in
    our master hashes that map fingerprints
    to instances of this class."""
    def __init__(self, chunk_index, filename):
        self.chunk_index = chunk_index
        self.filename = filename

    def __str__(self):
        return "Chunk: {c}, File: {f}".format(c=self.chunk_index, f=self.filename)


class MatchResult:
    """The result of comparing two files."""
    def __init__(self, file1, file2, score):
        self.file1 = file1
        self.file2 = file2
        self.score = score

    def __str__(self):
        short_file1 = os.path.basename(self.file1)
        short_file2 = os.path.basename(self.file2)
        match_string = "MATCH" if self.score > SCORE_THRESHOLD else "NO MATCH"
        return "{m}: {f1} {f2} ({s})".format(m=match_string, f1=short_file1, f2=short_file2, s=self.score)

def _to_fingerprints(freq_chunks):
    """Examine the results of running chunks of audio
    samples through FFT. For each chunk, look at the frequencies
    that are loudest in each "bucket." A bucket is a series of
    frequencies. Return the indices of the loudest frequency in each
    bucket in each chunk. These indices will be encoded into
    a single number per chunk."""
    chunks = len(freq_chunks)
    fingerprints = np.zeros(chunks, dtype=np.uint32)
    # Examine each chunk independently
    for chunk in xrange(chunks):
        fingerprint = 0
        for bucket in range(BUCKETS):
            start_index = bucket * BUCKET_SIZE
            end_index = (bucket + 1) * BUCKET_SIZE
            bucket_vals = freq_chunks[chunk][start_index:end_index]
            max_index = bucket_vals.argmax()
            fingerprint += (max_index << (bucket * BITS_PER_NUMBER))
        fingerprints[chunk] = fingerprint

    # return the indexes of the loudest frequencies
    return fingerprints


def _file_fingerprint(filename):
    """Read the samples from the files, run them through FFT,
    find the loudest frequencies to use as fingerprints,
    turn those into a hash table.
    Returns a 2-tuple containing the length
    of the file in seconds, and the hash table."""

    # Open the file
    file = InputFile(filename)

    # Read samples from the input files, divide them
    # into chunks by time, and convert the samples in each
    # chunk into the frequency domain.
    # The chunk size is dependent on the sample rate of the
    # file. It is important that each chunk represent the
    # same amount of time, regardless of the sample
    # rate of the file.
    chunk_size_adjust_factor = (NORMAL_SAMPLE_RATE / file.get_sample_rate())
    fft = FFT(file, int(NORMAL_CHUNK_SIZE / chunk_size_adjust_factor))
    series = fft.series()
    
    file_len = file.get_total_samples() / file.get_sample_rate()

    file.close()

    # Find the indices of the loudest frequencies
    # in each "bucket" of frequencies (for every chunk).
    # These loud frequencies will become the
    # fingerprints that we'll use for matching.
    # Each chunk will be reduced to a tuple of
    # 4 numbers which are 4 of the loudest frequencies
    # in that chunk.
    # Convert each tuple in winners to a single
    # number. This number is unique for each possible
    # tuple. This hopefully makes things more
    # efficient.
    fingerprints = _to_fingerprints(series)

    return FileResult(fingerprints, file_len, filename)


class Wang:
    """Create an instance of this class to use our matching system."""

    def __init__(self, dir1, dir2):
        """The two arguments should be strings that are
        file or directory paths. For files, we will simply
        examine these files. For directories, we will scan
        them for files."""
        self.dir1 = dir1
        self.dir2 = dir2

    @staticmethod
    def __search_dir(dir):
        """Returns the regular files residing
        in the given directory, OR if the input
        is a regular file, return a 1-element
        list containing this file. All paths
        returned will be absolute paths."""

        results = []
        # Get the absolute path of our search dir
        abs_dir = os.path.abspath(dir)
        # Get info about the directory provide
        dir_stat = os.stat(abs_dir)

        # If it's really a file, just
        # return the name of it
        if stat.S_ISREG(dir_stat.st_mode):
            results.append(abs_dir)
            return results

        # If it's neither a file nor directory,
        # bail out
        if not stat.S_ISDIR(dir_stat.st_mode):
            die("{d} is not a directory or a regular file.".format(d=abs_dir))

        # Scan through the contents of the
        # directory (non-recursively).
        contents = os.listdir(abs_dir)
        for node in contents:
            abs_node = abs_dir + os.sep + node
            node_stat = os.stat(abs_node)
            # If we find a regular file, add
            # that to our results list, otherwise
            # warn the user.
            if stat.S_ISREG(node_stat.st_mode):
                results.append(abs_node)
            else:
                warn("An inode that is not a regular file was found at {f}".format(abs_node))

        return results

    @staticmethod
    def __combine_hashes(files):
        """Take a list of FileResult objects and
        create a hash that maps all of their fingerprints
        to ChunkInfo objects."""
        master = defaultdict(list)
        for f in files:
            for chunk in xrange(len(f.fingerprints)):
                hash = f.fingerprints[chunk]
                master[hash].append(ChunkInfo(chunk, f.filename))

        return master

    @staticmethod
    def __file_lengths(files):
        """Take a list of FileResult objects and
        create a hash that maps their filenames
        to the length of each file, in seconds."""
        results = {}
        for f in files:
            results[f.filename] = f.file_len

        return results

    @staticmethod
    def __report_file_matches(file, master_hash, file_lengths):
        """Find files from the master hash that match
        the given file.
        @param file A FileResult object that is our query
        @param master_hash The data to search through
        @param file_lengths A hash mapping filenames to file lengths
        @return A list of MatchResult objects, one for every file
        that was represented in master_hash"""

        results = []

        # A hash that maps filenames to "offset" hashes. Then,
        # an offset hash maps the difference in chunk numbers of
        # the matches we will find.
        # We'll map those differences to the number of matches
        # found with that difference.
        # This allows us to see if many fingerprints
        # from different files occurred at the same
        # time offsets relative to each other.
        file_match_offsets = {}
        for f in file_lengths:
            file_match_offsets[f] = defaultdict(lambda: 0)

        # For each chunk in the query file
        for query_chunk_index in xrange(len(file.fingerprints)):
            # See if that chunk's fingerprint is in our master hash
            chunk_fingerprint = file.fingerprints[query_chunk_index]
            if chunk_fingerprint in master_hash:
                # If it is, record the offset between our query chunk
                # and the found chunk
                for matching_chunk in master_hash[chunk_fingerprint]:
                    offset = matching_chunk.chunk_index - query_chunk_index
                    file_match_offsets[matching_chunk.filename][offset] += 1

        # For each file that was in master_hash,
        # we examine the offsets of the matching fingerprints we found
        for f in file_match_offsets:
            offsets = file_match_offsets[f]

            # The length of the shorter file is important
            # to deciding whether two audio files match.
            min_len = min(file_lengths[f], file.file_len)

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

            results.append(MatchResult(file.filename, f, score))

        return results


    def match(self, debug=False, verbose=False):
        """Takes two AbstractInputFiles as input,
        and returns a boolean as output, indicating
        if the two files match."""

        dir1_files = Wang.__search_dir(self.dir1)
        dir2_files = Wang.__search_dir(self.dir2)

        # Try to determine how many
        # processors are in the computer
        # we're running on, to determine
        # the appropriate amount of parallelism
        # to use
        try:
            cpus = multiprocessing.cpu_count()
        except NotImplementedError:
            cpus = 1
        # Construct a process pool to give the task of
        # fingerprinting audio files
        pool = multiprocessing.Pool(cpus)
        try:
            # Get the fingerprints from each input file.
            # Do this using a pool of processes in order
            # to parallelize the work neatly.
            map1_result = pool.map_async(_file_fingerprint, dir1_files)
            map2_result = pool.map_async(_file_fingerprint, dir2_files)
            pool.close()

            # Get results from process pool
            dir1_results = map1_result.get()
            dir2_results = map2_result.get()

        except KeyboardInterrupt:
            pool.terminate()
            raise

        dir2_master_hash = Wang.__combine_hashes(dir2_results)
        dir2_file_lengths = Wang.__file_lengths(dir2_results)

        results = []

        # Loop through each file in the first search path our
        # program was given.
        for file in dir1_results:
            # For each file, check its fingerprints against those in the
            # second search path. For matching
            # fingerprints, look up the the times (chunk number)
            # that the fingerprint occurred
            # in each file. Store the time differences in
            # offsets. The point of this is to see if there
            # are many matching fingerprints at the
            # same time difference relative to each
            # other. This indicates that the two files
            # contain similar audio.
            file_matches = Wang.__report_file_matches(file, dir2_master_hash, dir2_file_lengths)
            for match_result in file_matches:
                results.append(match_result)

        return results

