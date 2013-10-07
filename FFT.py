import numpy.fft


class FFT:

    def __init__(self, input_file, chunk_size=2940):
        self.input_file = input_file
        self.chunk_size = chunk_size

    def series(self, chunks=-1):
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
        return float(self.input_file.get_sample_rate()) / float(self.chunk_size)