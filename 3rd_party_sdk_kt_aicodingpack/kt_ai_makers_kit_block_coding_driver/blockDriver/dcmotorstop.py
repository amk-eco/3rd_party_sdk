from time import sleep
import sys
import serial
ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
ser.close()
ser.open()

def sendPacketMRTEXE(exeIndex):
	packet_buff=[0xff,0xff,0x4c,0x53,0x00,0x00,0x00,0x00,0x30,0x0c,0x03,exeIndex,0x00,100,0x00];
	aa = range(6,14)
	for i in aa :
		packet_buff[14]= packet_buff[14] + packet_buff[i]
	arr = bytearray(packet_buff)
	print ser.write(arr)
	return

def dcMotorStop():
	packet_buff=['X','R',0, 0,0, 0,0, 0,'S']
	arr = bytearray(packet_buff)
	print ser.write(arr)
	return

def	main():
	dcMotorStop()
	sendPacketMRTEXE(2)

if __name__	== '__main__':
	main()