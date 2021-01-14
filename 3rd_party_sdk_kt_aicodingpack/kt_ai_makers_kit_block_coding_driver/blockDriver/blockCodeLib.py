#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import urllib3
import requests
import json
import grpc
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import gkit
import os
import datetime
import hmac
import hashlib
import pyaudio
import audioop
from six.moves import queue
from ctypes import *
import RPi.GPIO as GPIO
import ktkws # KWS
import wave
import subprocess
from time import sleep
import itertools
import os
import threading
import Adafruit_DHT
import smbus
import time

#remove warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

pin2bcm = {3:2, 5:3, 7:4, 8:14, 10:15, 11:17, 12:18, 13:27, 15:22, 16:23, 18:24, 19:10, 21:9, 22:25, 23:11, 24:8, 26:7, 29:5, 31:6, 32:12, 33:13, 35:19, 36:16, 37:26, 38:20, 40:21}
class LED:
    """Starts a background thread to show patterns with the LED.

  Simple usage:
    my_led = LED(channel = 31)
    my_led.start()
    my_led.set_state(LED.ON)
    my_led.stop()
  """

    OFF = 0
    ON = 1
    BLINK = 2
    BLINK_3 = 3
    BEACON = 4
    BEACON_DARK = 5
    DECAY = 6
    PULSE_SLOW = 7
    PULSE_QUICK = 8

    def __init__(self, channel):
        self.animator = threading.Thread(target=self._animate)
        self.channel = channel
        self.iterator = None
        self.running = False
        self.state = None
        self.sleep = 0

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(channel, GPIO.OUT)
        self.pwm = GPIO.PWM(channel, 100)

        self.lock = threading.Lock()

    def start(self):
        """Starts the LED driver."""
        with self.lock:
            if not self.running:
                self.running = True
                self.pwm.start(0)  # off by default
                self.animator.start()

    def stop(self):
        """Stops the LED driver and sets the LED to off."""
        with self.lock:
            if self.running:
                self.running = False
                """self.animator.join(2)"""
                """self.animator.stop()"""
                self.pwm.stop()

    def set_state(self, state):
        """Sets the LED driver's new state.

    Note the LED driver must be started for this to have any effect.
    """
        with self.lock:
            self.state = state

    def _animate(self):
        while True:
            state = None
            running = False
            with self.lock:
                state = self.state
                self.state = None
                running = self.running
            if not running:
                return
            if state is not None:
                if not self._parse_state(state):
                    raise ValueError('unsupported state: %d' % state)
            if self.iterator:
                self.pwm.ChangeDutyCycle(next(self.iterator))
                sleep(self.sleep)
            else:
                # We can also wait for a state change here with a Condition.
                sleep(1)

    def _parse_state(self, state):
        self.iterator = None
        self.sleep = 0.0
        if state == self.OFF:
            self.pwm.ChangeDutyCycle(0)
            return True
        if state == self.ON:
            self.pwm.ChangeDutyCycle(100)
            return True
        if state == self.BLINK:
            self.iterator = itertools.cycle([0, 100])
            self.sleep = 0.5
            return True
        if state == self.BLINK_3:
            self.iterator = itertools.cycle([0, 100] * 3 + [0, 0])
            self.sleep = 0.25
            return True
        if state == self.BEACON:
            self.iterator = itertools.cycle(
                itertools.chain([30] * 100, [100] * 8, range(100, 30, -5)))
            self.sleep = 0.05
            return True
        if state == self.BEACON_DARK:
            self.iterator = itertools.cycle(
                itertools.chain([0] * 100, range(0, 30, 3), range(30, 0, -3)))
            self.sleep = 0.05
            return True
        if state == self.DECAY:
            self.iterator = itertools.cycle(range(100, 0, -2))
            self.sleep = 0.05
            return True
        if state == self.PULSE_SLOW:
            self.iterator = itertools.cycle(
                itertools.chain(range(0, 100, 2), range(100, 0, -2)))
            self.sleep = 0.1
            return True
        if state == self.PULSE_QUICK:
            self.iterator = itertools.cycle(
                itertools.chain(range(0, 100, 5), range(100, 0, -5)))
            self.sleep = 0.05
            return True
        return False


KWSID = ['기가지니', '지니야', '친구야', '자기야']

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  dummy_var = 0
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 512

#/home/pi/blockcoding/kt_ai_makers_kit_block_coding_driver/blockDriver/key
with open("/home/pi/blockcoding/kt_ai_makers_kit_block_coding_driver/blockDriver/key/clientKey.json") as json_data_str:
    ClientData = json.load(json_data_str)


# Config for GiGA Genie gRPC
CLIENT_ID = ClientData["clientId"]
CLIENT_KEY = ClientData["clientKey"]
CLIENT_SECRET = ClientData["clientSecret"]
HOST = 'gate.gigagenie.ai'
PORT = 4080


### COMMON : Client Credentials ###
def getMetadata():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    message = CLIENT_ID + ':' + timestamp

    signature = hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

    metadata = [('x-auth-clientkey', CLIENT_KEY),
                ('x-auth-timestamp', timestamp),
                ('x-auth-signature', signature)]

    return metadata

def credentials(context, callback):
    callback(getMetadata(), None)

def getCredentials():
    with open('/home/pi/ai-makers-kit/data/ca-bundle.pem', 'rb') as f:
        trusted_certs = f.read()
    sslCred = grpc.ssl_channel_credentials(root_certificates=trusted_certs)

    authCred = grpc.metadata_call_credentials(credentials)

    return grpc.composite_channel_credentials(sslCred, authCred)

### END OF COMMON ###

# MicrophoneStream - original code in https://goo.gl/7Xy3TT
class MicrophoneStream(object):
	"""Opens a recording stream as a generator yielding the audio chunks."""
	def __init__(self, rate, chunk):
		self._rate = rate
		self._chunk = chunk

		# Create a thread-safe buffer of audio data
		self._buff = queue.Queue()
		self.closed = True

	def __enter__(self):
		self._audio_interface = pyaudio.PyAudio()
		self._audio_stream = self._audio_interface.open(
			format=pyaudio.paInt16,
			channels=1, rate=self._rate,
			input=True, frames_per_buffer=self._chunk,
			# Run the audio stream asynchronously to fill the buffer object.
			# This is necessary so that the input device's buffer doesn't
			# overflow while the calling thread makes network requests, etc.
			stream_callback=self._fill_buffer,
		)

		self.closed = False

		return self

	def __exit__(self, type, value, traceback):
		self._audio_stream.stop_stream()
		self._audio_stream.close()
		self.closed = True
		# Signal the generator to terminate so that the client's
		# streaming_recognize method will not block the process termination.
		self._buff.put(None)
		self._audio_interface.terminate()

	def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
		"""Continuously collect data from the audio stream, into the buffer."""
		self._buff.put(in_data)
		return None, pyaudio.paContinue

	def generator(self):
		while not self.closed:
			# Use a blocking get() to ensure there's at least one chunk of
			# data, and stop iteration if the chunk is None, indicating the
			# end of the audio stream.
			chunk = self._buff.get()
			if chunk is None:
				return
			data = [chunk]

			# Now consume whatever other data's still buffered.
			while True:
				try:
					chunk = self._buff.get(block=False)
					if chunk is None:
						return
					data.append(chunk)
				except queue.Empty:
					break

			yield b''.join(data)
# [END audio_stream]

def play_file(fname):
  wf = wave.open(fname, 'rb')
  wave_data = wf.readframes(wf.getnframes())
  audio = pyaudio.PyAudio()
  stream_out = audio.open(
      format=audio.get_format_from_width(wf.getsampwidth()),
      channels=wf.getnchannels(),
      rate=wf.getframerate(), input=False, output=True)
  stream_out.start_stream()
  stream_out.write(wave_data)
  sleep(0.2)
  stream_out.stop_stream()
  stream_out.close()
  audio.terminate() 

def ktkwsdetect():
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()

        for content in audio_generator:
            rc = ktkws.detect(content)
            rms = audioop.rms(content,2)
            #print('audio rms = %d' % (rms))
            if (rc == 1):
                #play_file("../data/sample_sound.wav")
                return 200

def setKTKws(key_index = 0):
    key_word = ['기가지니','지니야','친구야','자기야']
    rc = ktkws.init("/home/pi/ai-makers-kit/data/kwsmodel.pack")
    print ('init rc = %d' % (rc))
    rc = ktkws.start()
    print ('start rc = %d' % (rc))
    print ('\n호출어를 불러보세요~\n')
    ktkws.set_keyword(KWSID.index(key_word[key_index]))
    rc = ktkwsdetect()
    print ('detect rc = %d' % (rc))
    print ('\n\n호출어가 정상적으로 인식되었습니다.\n\n')
    ktkws.stop()
    return rc

def generate_request(): #for STT

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
    
        for content in audio_generator:
            message = gigagenieRPC_pb2.reqVoice()
            message.audioContent = content
            yield message
            
            rms = audioop.rms(content,2)
            # print_rms(rms)

def getVoice2Text(): #STT
    print ("\n\n음성인식을 시작합니다.\n\n\n")

    channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), getCredentials())
    stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)
    request = generate_request()
    resultText = ''
    for response in stub.getVoice2Text(request):
        if response.resultCd == 200: # partial
            print('resultCd=%d | recognizedText= %s' % (response.resultCd, response.recognizedText))
            resultText = response.recognizedText
        elif response.resultCd == 201: # final
            print('resultCd=%d | recognizedText= %s' % (response.resultCd, response.recognizedText))
            resultText = response.recognizedText
            break
        else:
            print('resultCd=%d | recognizedText= %s' % (response.resultCd, response.recognizedText))
            break

    print ("\n\n인식결과: %s \n\n\n" % (resultText).encode('utf-8'))
    if resultText == None:
      resultText = ""
    return resultText

# TTS : getText2VoiceStream
def getText2VoiceStream(inText):
    if len(inText) < 1 :
        return False
    print(inText)
    channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), getCredentials())
    stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)

    message = gigagenieRPC_pb2.reqText()
    message.lang=0
    message.mode=0
    message.text=inText

    with open("tts.wav",'wb' ) as writeFile:
        for response in stub.getText2VoiceStream(message):
            if response.HasField("resOptions"):
                print ("\n\nResVoiceResult: %d" %(response.resOptions.resultCd))
            if response.HasField("audioContent"):
                print ("Audio Stream\n\n")
                writeFile.write(response.audioContent)
    # player = gkit.WavePlayer()
    # player.load_audio("tts.wav")
    # player.play_audio()
    play_file("tts.wav")
            
    return response.resOptions.resultCd


def generate_request_dss():
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        messageReq = gigagenieRPC_pb2.reqQueryVoice()
        messageReq.reqOptions.lang=0
        messageReq.reqOptions.userSession=CLIENT_ID
        messageReq.reqOptions.deviceId=CLIENT_SECRET
        yield messageReq
        for content in audio_generator:
            message = gigagenieRPC_pb2.reqQueryVoice()
            message.audioContent = content
            yield message
            rms = audioop.rms(content,2)

def queryByVoice():
    print ("\n\n\n질의할 내용을 말씀해 보세요.\n\n듣고 있는 중......\n")
    #print ("종료하시려면 Ctrl+\ 키를 누르세요.")
    channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), getCredentials())
    stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)
    request = generate_request_dss()
    resultText = ''
    response = stub.queryByVoice(request)
    #print("\n\nresultCd: %d\n\n" % (response.resultCd))
    if response.resultCd == 200:
        print("질의 내용: %s" % (response.uword).encode('utf-8'))
        for a in response.action:
            response = (a.mesg)
            print(response)
            parsing_resp = response.replace('<![CDATA[', '')
            parsing_resp = parsing_resp.replace(']]>', '')
            resultText = parsing_resp
            print("\n질의에 대한 답변: " + parsing_resp +'\n\n\n')
            #print (a.actType)
            getText2VoiceStream(resultText)
    else:
        print("\n\nresultCd: %d\n" % (response.resultCd))
        print("정상적인 음성인식이 되지 않았습니다.")
        getText2VoiceStream("정상적인 음성인식이 되지 않았습니다.")
        #print("Fail: %d" % (response.resultCd))	
    return resultText
    
def detectKTBtn():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setwarnings(False)
  GPIO.setup(29, GPIO.IN,	pull_up_down=GPIO.PUD_UP)
  while True:
    input_value =	GPIO.input(29)
    if not input_value:
      print("detect Push Btn")
      break
    sleep(0.05)
  return True
# def get_led():
#       GPIO_LED = 31
#   global _gkit_led
#   if _gkit_led is None:
#       _gkit_led = LED(channel=GPIO_LED)
#       _gkit_led.start()
#   return _gkit_led

def setLED(ledType,duration):
  print("start led:%d duration:%d" % (ledType,duration))
  GPIO_LED = 31
  led = LED(channel=GPIO_LED)
  led.start()
  led.set_state(ledType)
  sleep(duration)
  print("stop led")
  led.stop()

def setGPIOMode(pin,mode):
  GPIO.setmode(GPIO.BOARD)
  GPIO.setwarnings(False)
  if mode == 1 :
    GPIO.setup(pin, GPIO.IN,	pull_up_down=GPIO.PUD_UP)
  else :
    GPIO.setup(pin, GPIO.OUT)

def gpioWrite(pin,value):
  setGPIOMode(pin,0)
  GPIO.output(pin,value)
def gpioRead(pin):
  setGPIOMode(pin,1)
  return GPIO.input(pin)

def getAPIPM10(city):
  URL = 'https://genieblock.kt.co.kr:3000/api/getPM'
  params = {'sido':city}
  response = requests.get(URL,params=params,verify=False)
  json_data = json.loads(response.text)
  return json_data["pm10"]

def getAPIPM25(city):
  URL = 'https://genieblock.kt.co.kr:3000/api/getPM'
  params = {'sido':city}
  response = requests.get(URL,params=params,verify=False)
  json_data = json.loads(response.text)
  return json_data["pm25"]

def setServo(pin,angle):
  print("setServo")
  FIFO = open('/dev/pi-blaster', 'w')
  minPulse = 0.06
  maxPulse = 0.19
  angle = float(angle)
  calPulse = minPulse + (maxPulse * (angle / 180))
  s = "%s=%s\n" % (pin2bcm[pin], calPulse)
  FIFO.write(s)
  

def getDHT11Temp(pin):
  humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin2bcm[pin])
  return temperature
def getDHT11Humidity(pin):
  humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin2bcm[pin])
  return humidity
def bh1750Lightlevel():
  bus = smbus.SMBus(1)
  data = bus.read_i2c_block_data(0x23,0x10)
  result=(data[1] + (256 * data[0])) / 1.2
  return result
def getBH1750():
  bh1750Lightlevel()
  time.sleep(0.5)
  return bh1750Lightlevel()
def main():
	# ktkwsStart()
  # getVoice2Text()
  # getText2VoiceStream("안녕하세요 이건 먼가요?..")
  # queryByVoice()   
  # detectKTBtn()
  # ktaimk_set_led(2,5)
  # gpioWrite(31,False)
  # print(getAPIPM10("서울"))
  # print(getAPIPM25("서울"))
  # print(getDHT11Temp(5))
  # print(getDHT11Humidity(5))
  # setServo(7,7.5)
  print("hello block-coding")

if __name__ == '__main__':
	main()