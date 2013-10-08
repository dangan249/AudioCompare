import sys
from WavInputFile import WavInputFile
import FFT
from Tkinter import *
import math


LOWER_LIMIT = 0
UPPER_LIMIT = 300
CHUNK_SIZE = 1024
RANGE = [40, 80, 120, 180, UPPER_LIMIT+1]

def get_bucket(freq):
    i = 0
    while RANGE[i] < freq:
        i += 1
    return i

def timestamp(chunk, chunk_size, samples_per_second):
    return float(chunk) * float(chunk_size) / float(samples_per_second)

def visualizer():
    """Display a graph that shows which frequencies we
    will use in our hashing algorithm.
    """
    try:
        input_file = WavInputFile(sys.argv[1])
    except IOError, e:
        print ("ERROR: {e}".format(e=e))
        return

    freq_chunks = FFT.FFT(input_file).series()

    # see fft_test for comments about this section
    chunks = len(freq_chunks)
    max = []
    max_index = []
    hashes = {}
    for chunk in range(chunks):
        max.append([])
        max_index.append([])
        for freq in range(LOWER_LIMIT, UPPER_LIMIT):
            mag = math.log(math.fabs(freq_chunks[chunk][freq])+1)
            bucket = get_bucket(freq)
            if len(max[chunk]) <= bucket:
                max[chunk].append(mag)
                max_index[chunk].append(max_index)
            if mag > max[chunk][bucket]:
                max[chunk][bucket] = mag
                max_index[chunk][bucket] = freq
        time = timestamp(chunk, CHUNK_SIZE, input_file.get_sample_rate())
        hash = "".join(["{:02.2f}".format(m) for m in max[chunk]])
        print hash
        hashes[hash] = time

    # initialize an empty window
    master = Tk()
    lines = UPPER_LIMIT
    blockSizeX = 3
    blockSizeY = 2
    w = Canvas(master, width=chunks*blockSizeX, height=lines*blockSizeY)
    w.pack()
    # for each chunk (which will be the X axis)
    for i in range(chunks):
        freq = 1
        # for each line (the Y axis)
        for line in range(1, lines):
            # see if the current line one of our "winning"
            # frequencies that we're hasing on
            bucket = get_bucket(line)
            if max_index[i][bucket] == line:
                important = True
            else:
                important = False

            # compute what color this frequency should
            # appear as, based on its magnitude
            abs = math.fabs(freq_chunks[i][freq]+1)
            mag = math.log10(abs)

            # assign color to red if winning frequency,
            # otherwise some shade of blue
            if mag > 0:
                if not important:
                    color = "#00" + "{:02x}".format(int(mag*10)) + "{:02x}".format(int(mag*20))
                else:
                    color = "#FF0000"
                # make a small rectangle on the scren of the appropriate color
                w.create_rectangle(i*blockSizeX, line*blockSizeY, (i+1)*blockSizeX, (line+1)*blockSizeY, fill=color, width=0)

            # the next line will represent a frequency that is logarithmically bigger than this one
            freq += math.log10(line) * math.log10(line)

    mainloop()

if __name__ == "__main__":
    visualizer()