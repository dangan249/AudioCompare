import numpy as np
from pylab import specgram, window_none


class FFT:
    """A mechanism for identifying the dominant frequencies
    in time ranges in an audio file."""
    def __init__(self, input_file, chunk_size=1024):
        """Set up an file for FFT processing.
        The constructor doesn't actually do the processing.
        @param input_file The file we'll read audio data from. The should
        be a AbstractInputFile-like object
        @param chunk_size The size of the chunks to put through FFT."""
        self.input_file = input_file
        self.chunk_size = chunk_size

    def series(self, chunks=-1, f=-1):
        """Return the FFTs of samples of audio chunks. The number of FFT bins will be almost
        double the number of chunks, because we compute two bins per chunk, one that is
        halfway overlapping the next one.
        @param chunks The number of chunks to read and return. -1 means all. Must be positive number
        otherwise. If there isn't enough audio data to read all of these chunks, we may read less.
        @param f The number of frequency values to return per chunk. -1 means all. Must be positive number
        less than chunk size otherwise."""
        # handle EOFError?
        # is the window doing anything?
        if chunks == -1:
            chunks = self.input_file.get_total_samples() / self.chunk_size
        # get all the audio samples we'll be working with
        samples = self.input_file.get_audio_samples(chunks * self.chunk_size)
        # mix those samples down into one channel
        mixed_samples = FFT.__mix(samples)
        # numpy.specgram will perform many FFTs over the sample, using bins equal to the chunk size
        s = specgram(mixed_samples, NFFT=self.chunk_size, noverlap=self.chunk_size/2, window=np.hamming(self.chunk_size))
        # specgram returns a bunch of things, just take the important stuff
        freqs = s[0]
        if f != -1:
            freqs = freqs.take(range(f), axis=0)
        return freqs.transpose()

    def base_freq(self):
        """Returns the base frequency. This is the frequency corresponding
        to the first index in the arrays returned by series()(?)."""
        return float(self.input_file.get_sample_rate()) / float(self.chunk_size)

    @staticmethod
    def __mix(samples):
        """Mix an arbitrary number of channels into one."""
        result = np.zeros(samples.shape[1])
        channels = len(samples)
        for i in range(len(result)):
            sum = 0
            for j in range(channels):
                sum += samples[j][i]
            mean = sum / channels
            result[i] = mean

        return result