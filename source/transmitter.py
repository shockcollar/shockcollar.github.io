# PET998D remote transmitter, see https://shockcollar.github.io
import RPi.GPIO as GPIO
import time

# Connect transmitter to this RPI pin (GPIO 2, pin 3)
OUTPUT_PIN = 3

BIT_PATTERN = "1{}{}00110101001000100{}{}{}00"
DEVICE_ONE_PATTERN = "111"
DEVICE_TWO_PATTERN = "000"

# Measured pulse with in seconds
LONG_PULSE_LENGTH=0.00071
SHORT_PULSE_LENGTH=0.00018
PREAMBLE_HIGH_LENGTH=0.00140


def sendHigh():
                GPIO.output(OUTPUT_PIN, GPIO.HIGH)
                time.sleep(LONG_PULSE_LENGTH)
                GPIO.output(OUTPUT_PIN, GPIO.LOW)
                time.sleep(SHORT_PULSE_LENGTH)

def sendLow():
                GPIO.output(OUTPUT_PIN, GPIO.HIGH)
                time.sleep(SHORT_PULSE_LENGTH)
                GPIO.output(OUTPUT_PIN, GPIO.LOW)
                time.sleep(LONG_PULSE_LENGTH)

# Creates binary fixed 7 bit length string
def createStrength(strength):
	return "{0:{fill}7b}".format(strength, fill='0')

def inverse(input):
	result = ""
	for c in input:
		if c == "1":
			result += "0"
		else:
			result += "1"
	return result

def getDevicePattern(device):
	if (device == 1):
		return DEVICE_ONE_PATTERN
	else:
		return DEVICE_TWO_PATTERN

def composePattern(strength, typePatternAtBeginning, typePatternAtEnd, device):
	devicePattern = getDevicePattern(device)
	return BIT_PATTERN.format(inverse(devicePattern), typePatternAtBeginning, strength, typePatternAtEnd, devicePattern)


# API
def createSoundInput(device=1):
	strength = createStrength(10) # sound can be any strength, remote sends 10
	typePatternAtBeginning = "0100"
	typePatternAtEnd = "1101"
	return composePattern(strength, typePatternAtBeginning, typePatternAtEnd, device)

def createVibrateInput(strength, device=1):
	strength = createStrength(strength)
	typePatternAtBeginning = "0010"
	typePatternAtEnd = "1011"
	return composePattern(strength, typePatternAtBeginning, typePatternAtEnd, device)

def createLampInput(device=1):
	strength = createStrength(10) # lamp can be any strength, remote sends 10
	typePatternAtBeginning = "1000"
	typePatternAtEnd = "1110"
	return composePattern(strength, typePatternAtBeginning, typePatternAtEnd, device)

def createShockInput(strength, device=1):
	strength = createStrength(strength)
	typePatternAtBeginning = "0001"
	typePatternAtEnd = "0111"
	return composePattern(strength, typePatternAtBeginning, typePatternAtEnd, device)

def init():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(OUTPUT_PIN, GPIO.OUT)

def destroy():
	GPIO.cleanup()


def send(input):
		GPIO.output(OUTPUT_PIN, GPIO.HIGH)
		time.sleep(PREAMBLE_HIGH_LENGTH)
		GPIO.output(OUTPUT_PIN, GPIO.LOW)
		time.sleep(LONG_PULSE_LENGTH)

		for c in input:
			if (c == "1"):
				sendHigh()
			else:
				sendLow()
		GPIO.output(OUTPUT_PIN, GPIO.LOW)


# Example usage:
init()
try:
	while True:
		i = 0
		while i < 3:
			input = createVibrateInput(10);
			#print input
			send(input)
			time.sleep(0.008)
			i += 1
		time.sleep(2)
finally:
	destroy()
