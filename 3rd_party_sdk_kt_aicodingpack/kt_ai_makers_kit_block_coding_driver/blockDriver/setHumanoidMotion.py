import sys
import serial
ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)

def setHumanoidMotion(motionIndex):
        packet_buff=[0xff,0xff,0x4c,0x53,0x00,0x00,0x00,0x00,0x30,0x0c,0x03,motionIndex,0x00,100,0x00];
        aa = range(6,14)
        for i in aa :
                packet_buff[14]= packet_buff[14] + packet_buff[i]

        print packet_buff
        arr = bytearray(packet_buff)
        print ser.write(arr)
        return

def     main(argv):
        args = [0]
        for i, arg_para in enumerate(argv):
                if i > 0:
                        args[i-1] = int(arg_para)
                        print("index: %d: position:%d" % (i,int(arg_para)))
        print(args)
        setHumanoidMotion( args[0] )

if __name__     == '__main__':
        main(sys.argv)




packet_buff=[0xff,0xff,0x4c,0x53,0x00,0x00,0x00,0x00,0x30,0x0c,0x03,motionIndex,0x00,100,0x00];
aa = range(6,14)
for i in aa :
        packet_buff[14]= packet_buff[14] + packet_buff[i]
arr = bytearray(packet_buff)
print ser.write(arr)
