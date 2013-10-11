import sys
from WavInputFile import WavInputFile
from Tkinter import *
import math
import numpy
from match_test import *
from FFT import FFT

CHUNK_SIZE = 8196

def visualizer():
    """Display a graph that shows which frequencies we
    will use in our hashing algorithm.
    """
    try:
        input_file = WavInputFile(sys.argv[1])
    except IOError, e:
        print ("ERROR: {e}".format(e=e))
        return

    freq_chunks = FFT(input_file).series()
    max_index = bucket_winners(freq_chunks)

    # initialize an empty window
    master = Tk()
    chunks = len(freq_chunks)
    lines = UPPER_LIMIT
    blockSizeX = 1
    blockSizeY = 3
    w = Canvas(master, width=chunks*blockSizeX, height=lines*blockSizeY)
    w.pack()
    # for each chunk (which will be the X axis)
    for i in range(chunks):
        # for each line (the Y axis)
        for line in range(0, lines):
            # compute what color this frequency should
            # appear as, based on its magnitude
            val = freq_chunks[i][line]
            abs = math.sqrt((val.real * val.real) + (val.imag * val.imag)) + 1
            mag = math.log(abs)

            # assign color to red if winning frequency,
            # otherwise some shade of grey
            bucket = get_bucket(line)
            if (line-LOWER_LIMIT) % BUCKET_SIZE == 0:
                color = "blue"
            elif line == max_index[i][bucket]:
                color = "red"
            else:
                color = "#{r:02x}{g:02x}{g:02x}".format(r=0, g=int(mag*10), b=int(mag*20))
            # make a small rectangle on the scren of the appropriate color
            w.create_rectangle(i*blockSizeX, line*blockSizeY, (i+1)*blockSizeX, (line+1)*blockSizeY, fill=color, width=0)

            # the next line will represent a frequency that is logarithmically bigger than this one
            #freq += 1#math.log10(line)# * math.log10(line)

    mainloop()

if __name__ == "__main__":
    visualizer()