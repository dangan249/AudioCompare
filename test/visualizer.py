import sys
from InputFile import InputFile
from Tkinter import *
from Matcher import *
import Matcher
from FFT import FFT
import numpy

from matplotlib.colors import LogNorm
import matplotlib.cm


NORMAL_CHUNK_SIZE = 1024
NORMAL_SAMPLE_RATE = 44100.0

def apply_bgcolor(a, r, g, b):
    bg_r = 0.0
    bg_g = 0.0
    bg_b = 0.0
    final_r = ((1 - a) * bg_r) + (a * r)
    final_g = ((1 - a) * bg_g) + (a * g)
    final_b = ((1 - a) * bg_b) + (a * b)
    return (final_r, final_g, final_b)

def visualizer():
    """Display a graph that shows which frequencies we
    will use in our hashing algorithm.
    """
    try:
        input_file = InputFile(sys.argv[1])
    except IOError, e:
        print ("ERROR: {e}".format(e=e))
        return

    sample_rate_adjust_factor = int(NORMAL_SAMPLE_RATE / input_file.get_sample_rate())

    freq_chunks = FFT(input_file, CHUNK_SIZE/sample_rate_adjust_factor).series()

    norm = LogNorm(0.000000001, numpy.amax(freq_chunks))

    winners = Matcher._bucket_winners(freq_chunks)

    # initialize an empty window
    master = Tk()
    master.wm_title(" ".join(sys.argv[1:]))
    chunks = len(freq_chunks)
    first_chunk = 0
    lines = UPPER_LIMIT
    blockSizeX = 2
    blockSizeY = 2
    w = Canvas(master, width=chunks*blockSizeX, height=lines*blockSizeY)
    w.pack()
    # for each chunk (which will be the X axis)
    for i in range(chunks):
        print i
        # for each line (the Y axis)
        for line in range(1, lines):
            # compute what color this frequency should
            # appear as, based on its magnitude
            val = freq_chunks[i+first_chunk][line]
            mag = norm(val)

            # assign color to red if winning frequency,
            # otherwise some shade of grey
            bucket = line / BUCKET_SIZE
            if (line) % BUCKET_SIZE == 0:
                color = "blue"
            elif line == winners[i][bucket]:
                color = "green"
            else:
                color_vals = matplotlib.cm.jet(mag)
                color_vals = apply_bgcolor(color_vals[0], color_vals[1], color_vals[2], color_vals[3])
                color = "#{r:02x}{g:02x}{g:02x}".format(r=int(color_vals[0]*255), g=int(color_vals[1]*255), b=int(color_vals[2]*255))
            # make a small rectangle on the screen of the appropriate color
            w.create_rectangle(i*blockSizeX, line*blockSizeY, (i+1)*blockSizeX, (line+1)*blockSizeY, fill=color, width=0)

    mainloop()

if __name__ == "__main__":
    visualizer()