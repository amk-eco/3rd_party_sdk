# from ozolib import ozolib
import ozolib
import time
import socket

DEBUG = False
def log(s):
    if DEBUG:
        print(s)

HOST='' 
PORT=50123 
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server_socket.bind((HOST,PORT))
except OSError as e:
    print(e)
    exit(1)
log("server started")

while True:
    server_socket.listen(1) 
    client_socket, addr=server_socket.accept()
    log('Connected by {}'.format(addr))
    data=client_socket.recv(1024)
    if data:
        data = data.decode('utf-8').lower()
        com = data.split(' ')
        param_cnt = len(com)
        log("com:{}, count:{}".format(com,param_cnt))
        if com[0] == 'connect':
            if 'bot1' in locals():  #이미 연결된 로봇이 있으면 연결안함
                if bot1.isconnected() is True:
                    ret = "Already Connencted"
                else:
                    del bot1
            if 'bot1' not in locals():
                ozo = ozolib.Ozo()
                if param_cnt>=2:
                    robot = ozo.find(com[1])
                else:
                    robot = ozo.find()   

                if robot is False:
                    ret = "None"
                else:
                    devices = ozo.getrobots()
                    log(robot)
                    log("Detected MAC&Names : {}".format(devices))
                    log("Selected MAC and Name : {}".format(robot))
                    bot1 = ozolib.Command(robot)
                    if bot1.connect() is False:
                        del bot1
                        ret = False
                    else:
                        ret = True

        elif com[0]=='disconnect':
            log("Disconnect 1")
            if 'bot1' in locals():  #연결된 로봇이 있는 경우만 disconnect
                log("Disconnect 2")                
                if bot1.isconnected() is True:
                    ret = bot1.disconnect()
                    log("bot1.disconnected")
                    del bot1
                else:
                    log("Disconnect 3")                     
                    del bot1
                    ret = True
            else:
                log("Disconnect 4") 
                ret = True

        elif com[0]=='isconnected':
            if 'bot1' not in locals():
                ret = False
            elif param_cnt==1:
                ret = bot1.isconnected()
            else:
                ret =  "Incorrect Parameters"  

        elif com[0]=='move':
            if 'bot1' not in locals():
                ret = "Not Connected"
            elif param_cnt==3:
                ret = bot1.move(int(com[1]),int(com[2]))
            elif param_cnt==4:
                ret = bot1.move(int(com[1]),int(com[2]),int(com[3]))
            else:
                ret =  "Incorrect Parameters"                  

        elif com[0]=='drive':
            if 'bot1' not in locals():
                ret = "Not Connected"            
            elif param_cnt == 2:              
                ret = bot1.drive(int(com[1]))
            else:
                ret =  "Incorrect Parameters"                  

        elif com[0]=='play':
            if 'bot1' not in locals():
                ret = "Not Connected"                 
            elif  param_cnt == 2:
                ret = bot1.play(com[1])
            else:
                ret =  "Incorrect Parameters"                

        elif com[0]=='turn':
            if 'bot1' not in locals():
                ret = "Not Connected"             
            elif param_cnt == 2:
                ret = bot1.turn(int(com[1]))
            else:
                ret =  "Incorrect Parameters"                  

        elif com[0]=='rotate':
            if 'bot1' not in locals():
                ret = "Not Connected"               
            elif param_cnt==2:
                ret = bot1.rotate(com[1])
            elif param_cnt==3:
                if com[2] == 'false':
                    ret = bot1.rotate(com[1], False)
                else:
                    ret = bot1.rotate(com[1], com[2])
            else:
                ret =  "Incorrect Parameters"                     

        elif com[0]=='stop':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==1:                           
                ret = bot1.stop()  
            else:
                ret =  "Incorrect Parameters"  

        elif com[0]=='onled':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==5:                           
                ret = bot1.onLED(int(com[1]),int(com[2]),int(com[3]),int(com[4]))  
            else:
                ret =  "Incorrect Parameters" 
                
        elif com[0]=='offled':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==1:                           
                ret = bot1.offLED()                  
            elif param_cnt==2:                           
                ret = bot1.offLED(int(com[1]))  
            else:
                ret =  "Incorrect Parameters" 

        elif com[0]=='rainbow':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==1:                           
                ret = bot1.rainbow()                  
            else:
                ret =  "Incorrect Parameters"     

        elif com[0]=='flashled':
            if 'bot1' not in locals():
                ret = "Not Connected"
            elif param_cnt==4:                           
                ret = bot1.flashLED(int(com[1]),int(com[2]),int(com[3]))                    
            elif param_cnt==5:                           
                ret = bot1.flashLED(int(com[1]),int(com[2]),int(com[3]),int(com[4]))                  
            else:
                ret =  "Incorrect Parameters"  
            log(ret)

        elif com[0]=='flashrainbow':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==1:                           
                ret = bot1.flashrainbow()                  
            elif param_cnt==2:                           
                 ret = bot1.flashrainbow(int(com[1]))                  
            else:
                ret =  "Incorrect Parameters"  

        elif com[0]=='dance':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==1:                           
                ret = bot1.dance()                  
            else:
                ret =  "Incorrect Parameters"                                                          

        elif com[0]=='gentone':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==2:                           
                ret = bot1.gentone(int(com[1]))                  
            elif param_cnt==3:                           
                 ret = bot1.gentone(int(com[1]),int(com[2])) 
            else:
                ret =  "Incorrect Parameters"                 

        elif com[0]=='zigzag':
            if 'bot1' not in locals():
                ret = "Not Connected"                  
            elif param_cnt==3:                           
                ret = bot1.zigzag(int(com[1]),int(com[2])) 
            elif param_cnt==4:
                if com[3] == 'false':
                    ret = bot1.zigzag(int(com[1]),int(com[2]),False)                  
                else:
                    ret = bot1.zigzag(int(com[1]),int(com[2])) 
            else:
                ret =  "Incorrect Parameters"                             

        elif com[0]=='turnoff':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==1:                           
                ret = bot1.turnoff()                  
            else:
                ret =  "Incorrect Parameters"                 

        elif com[0]=='readsensor':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==1:                           
                ret = bot1.readsensor()  
            elif param_cnt==2:                           
                ret = bot1.readsensor(float(com[1]))                                  
            else:
                ret =  "Incorrect Parameters"   

        elif com[0]=='version':
            if param_cnt==1:                           
                ret = ozolib.version()  
            else:
                ret =  "Incorrect Parameters"                                          

        elif com[0]=='quit':
            if 'bot1' in locals():
                if bot1.isconnected() is True:
                    ret = bot1.disconnect()
                else:
                    ret = True
            else:
                ret = True
            log("Quit {}".format(ret))
        else:
            ret="Unknown command"            

        log("Return:{}".format(ret))            
        client_socket.send(str(ret).encode())

    if data =='quit':       
        break
    
client_socket.close()    
server_socket.close()
log("server closed")
exit(0)
