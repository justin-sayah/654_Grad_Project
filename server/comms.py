import serial
from time import sleep

# ser = serial.Serial("COM3")
ser = serial.Serial("/dev/cu.usbserial-1410")

'''
Dimension should be 0 = x, 1 = y
duty_percent: 0 <= duty_percent <= 1

Receives position in one dimension 
NOT YET CONFIGURED WHICH ONE
'''
def send_duty(dimension, duty_percent):
    sleep(0.1)
    duty = (int)(900 + (duty_percent*1200))
    lowBitsSend, highBitsSend = (duty & 0xFFFFFFFF).to_bytes(2, 'big')
    testSend = [0, dimension, lowBitsSend, highBitsSend]
    byteSend = bytearray(testSend)
    ser.write(byteSend)
    lowByteRead = ser.read()
    highByteRead = ser.read()
    allBytes = lowByteRead + highByteRead
    dimensionRead = int.from_bytes(allBytes, 'big')
    return dimensionRead
