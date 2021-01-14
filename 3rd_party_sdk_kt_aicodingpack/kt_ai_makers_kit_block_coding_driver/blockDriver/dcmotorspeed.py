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


def dcMotorSpeed(L1, R1, L2, R2):
	if L1 < -10 : L1 = -10
	if R1 < -10 : R1 = -10
	if L2 > 10 : L2 = 10
	if R2 > 10 : R2 = 10
	
	if L1 < 0 : L1= 256+L1
	if L2 < 0 : L2= 256+L2
	if R1 < 0 : R1= 256+R1
	if R1 < 0 : R2= 256+R2
#  print 'MotorSpeed : L1:',L1, ',R1:', R1, ', L2:', L2, ',R2:', R2
	packet_buff=['X','R',0,L1, R1, L2, R2, 0,'S']
	arr = bytearray(packet_buff)
	print ser.write(arr)
	return
def dcMotorStop():
	packet_buff=['X','R',0, 0,0, 0,0, 0,'S']
	arr = bytearray(packet_buff)
	print ser.write(arr)
	return

def	 main(argv):
	postion = [0, 0, 0, 0]
	for i, motor_num in enumerate(argv):
		if i > 0:
			postion[i-1] = int(motor_num)
			print("index: %d: position:%d" % (i, int(motor_num)))
	print(postion)
	dcMotorSpeed(postion[0], postion[1], postion[2], postion[3])
	#dcMotorStop()
	sendPacketMRTEXE(2)

if __name__	== '__main__':
	main(sys.argv)
