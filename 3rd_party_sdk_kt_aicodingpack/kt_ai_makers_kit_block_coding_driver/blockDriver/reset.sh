#!/bin/sh

cd /home/pi/blockcoding
sudo rm -rf kt_ai_makers_kit_block_coding_driver/
git clone -b release --single-branch https://github.com/aimakers/blockcoding.git kt_ai_makers_kit_block_coding_driver
cd kt_ai_makers_kit_block_coding_driver/blockDriver/
mkdir key
npm install
