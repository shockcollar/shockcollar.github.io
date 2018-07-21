import pyaudio
from time import sleep

#Pyaudio
FORMAT = pyaudio.paUInt8
CHANNELS = 1
RATE = 48000
INPUT_BLOCK_TIME = 0.1
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

# Change under different sound card gain
HIGH = 120
LOW = 150

#Preamble
INITIAL_HIGH_LENGTH_SAMPLE=60
INITIAL_LOW_LENGTH_SAMPLE=30

# Read input state
block = None
blockIndex = 0

def readSignal():
    highStarts = 0
    i = 0
    while True:
      sample = readNextSample();
      if (i - highStarts) > INITIAL_HIGH_LENGTH_SAMPLE and sample < LOW:
        waitForLow();
        hightStarts = i
      if sample < LOW:
        highStarts = i
      i = i + 1

def waitForLow():
    i = 0
    while readNextSample() < HIGH:
        i += 1
    if i >= INITIAL_LOW_LENGTH_SAMPLE:
        readMessage()

def readMessage():
   print "readMessage"
   isProcessing = True
   result = "0"

   while isProcessing:
        success,bit = readOneBit()
        if success:
            result += bit
        else:
            isProcessing = False
   if (len(result) > 2): # otherwise probably noise
    print "Result: " + result

def readOneBit():
    # remove 0s
    j = 0
    while readNextSample() < HIGH:
        j += 1
        if (j > 60):
            return False,"x"

    i = 0
    while i < 60 and readNextSample() > LOW:
            i += 1
    if i > 5 and i < 60:
        if i < 15:
            result = "0"
        else:
            result = "1"
        return True,result
    else:
        return False,"x"

def readNextSample():
    global block
    global blockIndex
    if (block == None or blockIndex >= len(block)):
        blockIndex = 0
        try:
            block = stream.read(INPUT_FRAMES_PER_BLOCK)
        except IOError, e:
            print( "(%d) Error recording: %s"%(errorcount,e) )
    resultIndex = blockIndex
    blockIndex += 1
    return ord(block[resultIndex])

pa = pyaudio.PyAudio()

stream = pa.open(format = FORMAT,
         channels = CHANNELS,
         rate = RATE,
         input = True,
         frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

readSignal()
