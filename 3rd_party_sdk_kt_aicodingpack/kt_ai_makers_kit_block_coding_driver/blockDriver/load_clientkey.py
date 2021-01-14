#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
import json

url = "https://api.gigagenie.ai/api/v1/service/service"

body = "{\n\t\"categoryCode\" : \"AIMAK\",\n\t\"deviceGroup\" : \"3PD\",\n\t\"deviceTypeList\" : [\"EDUKIT\"],\n\t\"resourceTypeList\" : [\"DSS\",\"STT\",\"TTS\"]\n}"
headers = {
    'Accept': "application/json,text/plain,*/*",
    'Content-Type': "application/json",
    'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhaW1ha2VycyIsImF1dGhvcml0aWVzIjpbIlJPTEVfREVGQVVMVCJdLCJwbGF0Zm9ybSI6IkdpR0EgR2VuaWUgRGV2ZWxvcGVyIFBvcnRhbCIsImNsaWVudF9pZCI6ImJsb2NrY29kaW5nIiwicmVhbG5hbWUiOiJhaW1ha2VycyIsImF1ZCI6WyJBSVBPUlRBTCJdLCJsb2dpbkZhaWxDb3VudCI6MCwicmVxdWlyZWRDaGFuZ2VQd2QiOiJOIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImxhc3RQd2RDaGFuZ2VEYXRlIjoxNTU1ODkyNzM3NjYxLCJjb21wYW55Ijoia3QiLCJjbG91ZFVzZXIiOiJOIiwidXNlckRpdkNkIjoiVTAwMiIsImp0aSI6IjEyN2M1NzZiLTQ5MjMtNDVkYi1hZTU3LTRiYmJlMTI1NTM1NSJ9.dCIFKOkSW8j-A6VIoHvzElL17xwhheatU7CDSJDwkExLo22YGZJZSJdZeOg40OsXlmPbS9gvwttRkP5rt27FPx3MZKuwfIO5QoH1RVwQDVahVThl4pO3FImkIC9w_RS6BTRstbEiXJWL5rxKosDZEfA4KwJ_rDeOceTk7227PJscGe0TDQhysXks1smDo4D2nsbtP_b0SMjkIwO7117W0p48DHdmdpGv2RNE7_WTtNINvKh3j3MWWhzNEHvD3RBCXH5qZ80d_fB_Nvz-64F0jKo5tOU_di0o9_VP82lo-D7i6P6fuLIMB20HMjRT-NFQcRJY1cHuMeijb95G_PvCGg",
    'cache-control': "no-cache"
    }
 
try:
    response = requests.request("POST", url, data=body, headers=headers)
except requests.exceptions.RequestException:
    print ("네트워크가 연결 되어 있지 않습니다. 다시 한번 시도해 주세요.")
    exit(1)

response_text = response.text
key1 = json.loads(response_text)
key2 = key1["data"]["data"]
### print json.dumps(key2)

if key2["certUrl"] == "https://api.gigagenie.ai/api/v1/aiportal/cert":
    f = open('/home/pi/Downloads/clientKey.json', 'w')
    f.write (json.dumps(key2))
    f.close()
else:
    print ("네트워크가 연결 되어 있지 않습니다. 다시 한번 시도해 주세요.")


print ("API Key가 발급되었습니다. 무료로 하루에 1000건을 사용하실 수 있습니다. ")
print ("/home/pi/Downloads/clientKey.json 에 저장되었습니다. " )






