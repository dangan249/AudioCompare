import sys
from WavInputFile import WavInputFile
import FFT
from Tkinter import *
import math


LOWER_LIMIT = 0
UPPER_LIMIT = 300
CHUNK_SIZE = 4096
RANGE = [40, 80, 120, 180, UPPER_LIMIT+1]

def get_bucket(freq):
    i = 0
    while RANGE[i] < freq:
        i += 1
    return i

def visualizer():
    try:
        input_file = WavInputFile(sys.argv[1])
    except IOError, e:
        print ("ERROR: {e}".format(e=e))
        return

    freq_chunks = FFT.FFT(input_file).series()

    max = []
    max_index = []
    for chunk in range(len(freq_chunks)):
        max.append({})
        max_index.append({})
        #print chunk
        for freq in range(LOWER_LIMIT, UPPER_LIMIT):
            mag = math.log(math.fabs(freq_chunks[chunk][freq])+1)
            #mag_array.append(mag)
            bucket = get_bucket(freq)
            if not bucket in max[chunk]:
                max[chunk][bucket] = mag
                max_index[chunk][bucket] = freq
            if mag > max[chunk][bucket]:
                max[chunk][bucket] = mag
                max_index[chunk][bucket] = freq

    master = Tk()
    lines = UPPER_LIMIT
    blockSizeX = 3
    blockSizeY = 2
    w = Canvas(master, width=len(freq_chunks)*blockSizeX, height=lines*blockSizeY)
    w.pack()
    for i in range(len(freq_chunks)):
        freq = 1
        for line in range(1, lines):
            bucket = get_bucket(line)
            if max_index[i][bucket] == line:
                important = True
            else:
                important = False
            abs = math.fabs(freq_chunks[i][freq]+1)
            mag = math.log10(abs)
            if mag > 0:
                if not important:
                    color = "#00" + "{:02x}".format(int(mag*10)) + "{:02x}".format(int(mag*20))
                else:
                    color = "#FF0000"
                w.create_rectangle(i*blockSizeX, line*blockSizeY, (i+1)*blockSizeX, (line+1)*blockSizeY, fill=color, width=0)

            freq += 1#math.log10(line) * math.log10(line)

    mainloop()

if __name__ == "__main__":
    visualizer()