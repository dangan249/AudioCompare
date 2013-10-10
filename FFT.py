import numpy.fft
import scipy


class FFT:
    """A mechanism for identifying the dominant frequencies
    in time ranges in an audio file."""
    def __init__(self, input_file, chunk_size=8196):
        """Set up an file for FFT processing.
        The constructor doesn't actually do the processing."""
        self.input_file = input_file
        self.chunk_size = chunk_size

    def series(self, chunks=-1):
        """Returns an array of arrays. The outer array contains
         one array for each chunk of the file that
         we examine. Each chunk result in an array of numbers
         that describe the relative amplitude of certain
         frequencies within that chunk. The actual frequencies
         can be determined by the base frequency multiplied by the
         index in the array(?).
         If no number of chunks is specified, run over the entire file."""
        result = []
        if chunks == -1:
            chunks = self.input_file.get_total_samples() / self.chunk_size
        for i in range(chunks):
            try:
                samples = self.input_file.get_audio_samples(self.chunk_size)[0] # use channel 0
                result.append(numpy.fft.rfft(samples))
            except EOFError:
                break
        return result

    def base_freq(self):
        """Returns the base frequency. This is the frequency corresponding
        to the first index in the arrays returned by series()(?)."""
        return float(self.input_file.get_sample_rate()) / float(self.chunk_size)