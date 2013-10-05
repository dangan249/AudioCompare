
import sys
import WavInputFile

def audio_matcher():

    if len(sys.argv) < 3:
        print "Must provide two input files."
        return

    input_file_1 = WavInputFile(sys.argv[1])
    input_file_2 = WavInputFile(sys.argv[2])

#    input_file_1_normalized = normalize(input_file_1.audio_data())
#    input_file_2_normalized = normalize(input_file_2.audio_data())

#    input_file_1_fft = fft(input_file_1_normalized)
#    input_file_2_fft = fft(input_file_2_normalized)

#    if matcher(input_file_1_fft, input_file_2_fft):
#        print "MATCH"
#    else:
#        print "NO MATCH"

if __name__ == "__main__":
    audio_matcher()