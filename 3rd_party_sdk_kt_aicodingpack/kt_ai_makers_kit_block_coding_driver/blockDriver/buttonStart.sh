#!/bin/sh
sudo systemctl daemon-reload
sudo systemctl start aimk_auto.service
echo "Button 실행하기 기능을 켭니다...."
echo "Enter키를 누르면 종료합니다."
read choice; case "$choice" in *) exit; esac;