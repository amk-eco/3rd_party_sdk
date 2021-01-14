#!/bin/sh


count=$(find /home/pi/Downloads/ -maxdepth 1 -type f -name 'clientKey.json'| wc -l)  

echo "API Key Checking...." 

if [ $count -eq 0 ]; then 
   echo "API Key를 신규로 발급합니다. ";
          python /home/pi/blockcoding/kt_ai_makers_kit_block_coding_driver/blockDriver/load_clientkey.py 
   ## echo "API Key가 발급되었습니다. 무료로 하루에 1000건을 사용하실 수 있습니다. ";
   ## echo "/home/pi/Downloads/clientKey.json 에 저장되었습니다. ";
else 
   keyCheck=$(grep 'clientKey' /home/pi/Downloads/clientKey.json | wc -l)
   if [ $keyCheck -eq 0 ]; then
        echo "API Key를 다시 발급합니다.";
        rm /home/pi/Downloads/clientKey.json;
        python /home/pi/blockcoding/kt_ai_makers_kit_block_coding_driver/blockDriver/load_clientkey.py;
   else
        echo "API Key가 이미 발급 되어 있습니다. ";
   fi
fi
 
echo "Enter키를 누르면 종료합니다."
read choice; case "$choice" in *) exit; esac;

