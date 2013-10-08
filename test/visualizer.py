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
    try:
        input_file = WavInputFile(sys.argv[1])
    except IOError, e:
        print ("ERROR: {e}".format(e=e))
        return

    freq_chunks = FFT.FFT(input_file).series()

    chunks = len(freq_chunks)
    #max = [[copy.deepcopy(0) for y in range(len(RANGE))] for x in range(chunks)]
    #max_index = [[copy.deepcopy(0) for y in range(len(RANGE))] for x in range(chunks)]
    #max = [x[:] for x in [[0]*len(RANGE)]*chunks]
    #max_index = [x[:] for x in [[0]*len(RANGE)]*chunks]
    max = []
    max_index = []
    hashes = {}
    for chunk in range(chunks):
        #max.append([0 for _ in range(len(RANGE))])
        max.append([])
        max_index.append([])
        #max_index.append([0 for _ in range(len(RANGE))])
        #print chunk
        for freq in range(LOWER_LIMIT, UPPER_LIMIT):
            mag = math.log(math.fabs(freq_chunks[chunk][freq])+1)
            #mag_array.append(mag)
            #print chunk, freq
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

    #for r in max:
    #    print r

    return

    master = Tk()
    lines = UPPER_LIMIT
    blockSizeX = 3
    blockSizeY = 2
    w = Canvas(master, width=chunks*blockSizeX, height=lines*blockSizeY)
    w.pack()
    for i in range(chunks):
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

            freq += math.log10(line) * math.log10(line)

    mainloop()

if __name__ == "__main__":
    visualizer()