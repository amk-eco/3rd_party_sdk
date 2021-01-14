import sys
import serial


def     analogRead(port):
        ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
        tmp=ser.read(19)
        #print ' '.join(x.encode('hex') for x in tmp)
        start=tmp.find('\x52\x58\x3d\x00\x0e')
        if(port<0 or port>5):
                return
        print( ord(tmp[start+4+port]) )        


def     main(argv):
        args = [0]
        for i, arg_para in enumerate(argv):
                if i > 0:
                        args[i-1] = int(arg_para)
                        #print("index: %d: position:%d" % (i,int(arg_para)))
                        analogRead(args[0])

if __name__     == '__main__':
        main(sys.argv)
