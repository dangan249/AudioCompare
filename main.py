import sys
from WavInputFile import WavInputFile
import FFT


def audio_matcher():

    if len(sys.argv) < 3:
        print "Must provide two input files."
        return

    try:
        input_file_1 = WavInputFile(sys.argv[1])
        input_file_2 = WavInputFile(sys.argv[2])
    except IOError, e:
        print ("ERROR: {e}".format(e=e))
        return

#    input_file_1_normalized = normalize(input_file_1.audio_data())
#    input_file_2_normalized = normalize(input_file_2.audio_data())

#    input_file_1_fft = fft(input_file_1_normalized)
#    input_file_2_fft = fft(input_file_2_normalized)

#   I don't yet understand how audio fingerprints work, but here would
#   probably be where we'd generate them

#    if matcher(input_file_1_fft, input_file_2_fft):
#        print "MATCH"
#    else:
#        print "NO MATCH"

if __name__ == "__main__":
    audio_matcher()