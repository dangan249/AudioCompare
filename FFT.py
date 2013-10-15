import numpy.fft
import numpy
from pylab import specgram, window_none


class FFT:
    """A mechanism for identifying the dominant frequencies
    in time ranges in an audio file."""
    def __init__(self, input_file, chunk_size=8196):
        """Set up an file for FFT processing.
        The constructor doesn't actually do the processing."""
        self.input_file = input_file
        self.chunk_size = chunk_size

    def series(self):
        samples = self.input_file.get_audio_samples(self.input_file.get_total_samples())
        samples = numpy.array(samples[0])
        s = specgram(samples, NFFT=512, noverlap=0, window=numpy.hamming(512))
        return s[0].transpose()

    def series_raw(self):
        samples = self.input_file.get_audio_samples(self.input_file.get_total_samples())
        print samples[0][0:100]
        s = specgram(samples[0], NFFT=512, noverlap=0)
        return s

    def series2(self, chunks=-1, skip=0):
        """Returns an array of arrays. The outer array contains
         one array for each chunk of the file that
         we examine. Each chunk result in an array of numbers
         that describe the relative amplitude of certain
         frequencies within that chunk. The actual frequencies
         can be determined by the base frequency multiplied by the
         index in the array(?).
         If no number of chunks is specified, run over the entire file."""
        result = []
        if skip > 0:
            self.input_file.get_audio_samples(skip)
        if chunks == -1:
            chunks = self.input_file.get_total_samples() / self.chunk_size
        for i in range(chunks):
            try:
                samples = self.input_file.get_audio_samples(self.chunk_size)
                mixed_samples = FFT.__mix(samples)
                result.append(numpy.fft.rfft(mixed_samples))
            except EOFError:
                break
        return result

    def base_freq(self):
        """Returns the base frequency. This is the frequency corresponding
        to the first index in the arrays returned by series()(?)."""
        return float(self.input_file.get_sample_rate()) / float(self.chunk_size)

    @staticmethod
    def __mix(samples):
        """Mix an arbitrary number of channels into one."""
        result = [0 for _ in range(len(samples[0]))]
        channels = len(samples)
        for i in range(len(result)):
            sum = 0
            for j in range(channels):
                sum += samples[j][i]
            mean = sum / channels
            result[i] = mean

        return result

    @staticmethod
    def __hamming(M):
        if len(M) < 1:
            return numpy.array([])
        if len(M) == 1:
            return numpy.ones(1,float)
        n = numpy.arange(0,len(M))
        return 0.54-0.46*numpy.cos(2.0*numpy.pi*n/(len(M)-1))