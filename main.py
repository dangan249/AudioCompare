import sys
from WavInputFile import WavInputFile

def audio_matcher():

    if len(sys.argv) < 3:
        print "Must provide two input files."
        return

    # Open the two input files
    try:
        input_file_1 = WavInputFile(sys.argv[1])
        input_file_2 = WavInputFile(sys.argv[2])
    except IOError, e:
        print ("ERROR: {e}".format(e=e))
        return

#    if matcher(input_file_1_fft, input_file_2_fft):
#        print "MATCH"
#    else:
#        print "NO MATCH"

if __name__ == "__main__":
    audio_matcher()