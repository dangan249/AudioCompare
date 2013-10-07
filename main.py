import sys
from WavInputFile import WavInputFile
import FFT
from Tkinter import *
import math

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

    freq_chunks =  FFT.FFT(input_file_1.get_audio_samples(441000)[0])

    master = Tk()
    lines = 310
    blockSizeX = 3
    blockSizeY = 2
    w = Canvas(master, width=len(freq_chunks)*blockSizeX, height=lines*blockSizeY)
    w.pack()
    for i in range(len(freq_chunks)):
        freq = 1
        for line in range(1, lines):
            abs = math.fabs(freq_chunks[i][freq]+1)
            mag = math.log10(abs)
            if mag > 0:
                #print mag

                color = "#00" + "{:02x}".format(int(mag*10)) + "{:02x}".format(int(mag*20))
                #print color
                #w.create_rectangle(100, 100, 200, 200, fill="red")
                w.create_rectangle(i*blockSizeX, line*blockSizeY, (i+1)*blockSizeX, (line+1)*blockSizeY, fill=color, width=0)
                #print (i*blockSizeX, line*blockSizeY, (i+1)*blockSizeX, (line+1)*blockSizeY, color)

            freq += math.log10(line) * math.log10(line)

    mainloop()

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