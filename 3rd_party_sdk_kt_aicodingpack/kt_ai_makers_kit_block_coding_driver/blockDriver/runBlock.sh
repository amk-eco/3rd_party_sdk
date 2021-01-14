#!/bin/sh
sudo systemctl stop aimk_auto
count=$(find /home/pi/blockcoding/kt_ai_makers_kit_block_coding_driver/blockDriver/key/ -maxdepth 1 -type f -name 'clientKey.json'| wc -l)  

echo "API Key Checking...." 

if [ $count -eq 0 ]; then 
    echo "API Key를 신규로 발급합니다. ";
          python /home/pi/blockcoding/kt_ai_makers_kit_block_coding_driver/blockDriver/load_clientkey_bc.py
else 
   keyCheck=$(grep 'clientKey' /home/pi/blockcoding/kt_ai_makers_kit_block_coding_driver/blockDriver/key/clientKey.json | wc -l)
   if [ $keyCheck -eq 0 ]; then
        echo "API Key를 다시 발급합니다.";
        rm /home/pi/blockcoding/kt_ai_makers_kit_block_coding_driver/blockDriver/key/clientKey.json;
        python /home/pi/blockcoding/kt_ai_makers_kit_block_coding_driver/blockDriver/load_clientkey_bc.py;
   else
        echo "API Key가 이미 발급 되어 있습니다. ";
   fi
fi
  
setsid /usr/bin/chromium-browser --profile-directory=Default https://211.251.239.230:8443/  > /dev/null 2>&1 &
sudo node /home/pi/blockcoding/kt_ai_makers_kit_block_coding_driver/blockDriver/blockDriver2.js


