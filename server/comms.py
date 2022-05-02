import serial
from time import sleep

ser = serial.Serial("COM3")
# duty = 2100
# #dutyBytes = duty.to_bytes(2, 'big')
# y1, y2 = (duty & 0xFFFFFFFF).to_bytes(2, 'big')
# #print(dutyBytes)
# testSend = [0, 0, y1, y2]
# byteSend = bytearray(testSend)
# ser.write(byteSend)

'''
Dimension should be 0 = x, 1 = y
duty_percent: 0 <= duty_percent <= 1

Receives position in one dimension 
NOT YET CONFIGURED WHICH ONE
'''
def send_duty(dimension, duty_percent):
    duty = (int)(900 + (duty_percent*1200))
    lowBitsSend, highBitsSend = (duty & 0xFFFFFFFF).to_bytes(2, 'big')
    testSend = [0, dimension, lowBitsSend, highBitsSend]
    byteSend = bytearray(testSend)
    ser.write(byteSend)
    lowByteRead = ser.read()
    highByteRead = ser.read()
    allBytes = lowByteRead + highByteRead
    dimensionRead = int.from_bytes(allBytes, 'big')

    # print(allBytes)
    # #figure out how to combine bytes into 2 byte int
    # print(int.from_bytes(allBytes, 'big'))


while(1):
    send_duty(0, .5)
    sleep(1)
    send_duty(1, .5)
    sleep(1)
    # send_duty(1, 0)
    # sleep(1)
    # send_duty(0, 1)
    # sleep(1)
    # send_duty(1, 1)
    # sleep(1)