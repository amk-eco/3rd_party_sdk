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

def servoMotorAngle(pinNo, nAngle):

#  print 'nAngle := ', nAngle
  if(nAngle<-90) : nAngle = -90
  if(nAngle>90) : nAngle = 90
  if(nAngle<0): nAngle = 255+nAngle

  if pinNo<1 : pinNo = 1
  if pinNo>5 : pinNo = 5

  packet_buff=['X','R',3,pinNo, nAngle,0,0,0,'S']   # servo-motor angle 180 deg
  arr = bytearray(packet_buff)
  print ser.write(arr)
  return

def	main(argv):
	servo = [0, 0]
	for i, arg_para in enumerate(argv):
		if i > 0:
			servo[i-1] = int(arg_para)
			print("index: %d: position:%d" % (i,int(arg_para)))
	print(servo)
	servoMotorAngle(servo[0], servo[1])
	sendPacketMRTEXE(2)

if __name__	== '__main__':
	main(sys.argv)
