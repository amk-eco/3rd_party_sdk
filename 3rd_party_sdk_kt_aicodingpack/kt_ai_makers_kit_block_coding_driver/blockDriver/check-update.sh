#!/bin/sh
echo 권한 체크
whoami

echo 최신 업데이트 코드를 받습니다.

curl -kfsSL https://genieblock.kt.co.kr/update/update.sh -o update.sh && chmod +x ./update.sh && ./update.sh

echo 업데이트를 종료합니다. 아무키나 입력해 주세요
read var
