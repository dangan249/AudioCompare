import numpy.fft


def FFT(audio_data):
    return numpy.fft.rfft(audio_data)