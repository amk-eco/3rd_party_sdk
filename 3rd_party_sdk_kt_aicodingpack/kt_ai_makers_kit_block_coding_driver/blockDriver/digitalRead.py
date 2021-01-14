import sys
import serial

def     digitalRead(port):
        ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
        tmp=ser.read(19)
        #print ' '.join(x.encode('hex') for x in tmp)
        start=tmp.find('\x52\x58\x3d\x00\x0e')
        if(port<0 or port>5):
                return
        if(ord(tmp[start+4+port])>100) :
            print( 1 )
        else:
            print(0)


def     main(argv):
        args = [0]
        for i, arg_para in enumerate(argv):
                if i > 0:
                        args[i-1] = int(arg_para)
                        #print("index: %d: position:%d" % (i,int(arg_para)))
                        digitalRead(args[0])

if __name__     == '__main__':
        main(sys.argv)


