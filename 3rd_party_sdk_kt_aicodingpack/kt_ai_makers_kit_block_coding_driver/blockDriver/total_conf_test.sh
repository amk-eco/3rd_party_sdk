#!/bin/bash
RESULT=""
TMPDIR="/home/pi/Music"
CONFDIR="/home/pi/.genie-kit/bin"
WPA_CONF="/etc/wpa_supplicant/wpa_supplicant.conf"
IF_CONF="/tmp/ifconfig.txt"
wifi_conf=0

if pip list --format=legacy | grep "speedtest" > /dev/null; then
	echo ""
	echo "속도 측정 필수 패키지가 설치되었습니다."
	echo "사전 환경 점검 툴로 이동합니다. 엔터키를 쳐 주세요."
else
	echo ""
	echo "속도 측정 필수 패키지가 설치되지 않아 설치를 시작합니다."
	sudo pip install speedtest-cli
	echo "속도 측정 필수 패키지 설치를 완료하였습니다."
	echo "사전 환경 점검 툴로 이동합니다. 엔터키를 쳐 주세요."
fi

read choice;


while true
do
clear
echo ""
echo  "\e[0;31;42m\t\t\t\t\t\t\t\t\e[0m"
echo "\e[0;31;42m\t  [원활한 AMK 사용을 위한 사전 환경 점검]\t\t\e[0m"
echo "\e[0;31;42m\t\t\t\t\t\t\t\t\e[0m"
echo "\e[0;31;41m\t\t\t\t\t\t\t\t\e[0m"
echo "\e[1;37;41m1. 마이크 동작 테스트\t\t\t\t\t\t\e[0m"
echo "\e[1;37;41m2. 스피커 동작 테스트\t\t\t\t\t\t\e[0m"
echo "\e[1;37;41m3. Wi-Fi 설정 및 정상 연결 테스트\t\t\t\t\e[0m"
echo "\e[1;37;41m4. 인터넷 속도 테스트(블록코딩의 경우 5Mbps 이상의 속도 요구)\t\e[0m"
echo "\e[1;37;41m5. AMK 환경 테스트 종료\t\t\t\t\t\t\e[0m"
echo "\e[0;31;41m\t\t\t\t\t\t\t\t\e[0m"
echo ""
echo "메뉴선택 >>"
read menu

case "$menu" in
	[1]*)
	   echo "> 마이크 테스트를 진행합니다."
	   echo "> 엔터키를 누르면 녹음을 시작합니다."
	   read choice
    	   arecord -q -D plughw:0 -d 5 -c2 -r 48000 -f S16_LE -t wav $TMPDIR/.test.wav
	   aplay -q $TMPDIR/.test.wav
	   rm $TMPDIR/.test.wav
	   echo "> 방금 녹음된 소리를 들으셨나요?(Y/N)"
	   read choice2
	   case "$choice2" in
	   	[yY]*)
			echo  "\n마이크가 정상적으로 동작합니다."
			;;
		[nN]*)
			echo  "\n마이크 작동에 문제가 있습니다. 음성 기판 핀 연결 상태와 더불어 기판에\n마이크 선이 잘 연결되어 있는지 확인 바랍니다."
			;;
		esac
		read out
		;;
	[2]*)
		echo "> 재생 기능을 점검합니다."
		echo "> 엔터키를 누르면 음성을 재생합니다."
		read choice
		aplay -q -D plughw:0 $CONFDIR/sample_sound.wav
		echo "> 소리를 들으셨나요?(Y/N)"
		read choice
		case "$choice" in
			[yY]*)
				echo  "\n스피커가 정상적으로 동작합니다."
				;;
			[nN]*)
				echo  "\n스피커 작동에 문제가 있습니다. 음성 기판 핀 연결 상태와 더불어 기판에\n스피커 선이 잘 연결되어 있는지 확인 바랍니다."
				;;
		esac
		read out
		;;
	[3]*)
		echo ""
		echo  "Wi-Fi 설정 및 정상 연결 테스트를 진행합니다."
		echo ""
		echo  "\e[1;34m 1) Wi-Fi 설정 체크 \e[0m"
		if sudo cat $WPA_CONF|grep "network=" > /dev/null; then 
			echo  "  > Wi-Fi 설정이 있습니다";
			wifi_conf=1
		else 
			echo "> Wi-Fi 설정이 없습니다";
			echo "> 공유기(AP)와 연결 설정을 추가해 주세요";
			echo ""
			echo "> 엔터키를 누르면 메인 메뉴로 돌아갑니다."
			read choice; 
			case "$choice" in 
				*)
					;;
			esac
			wifi_conf=0
		fi
		if [ $wifi_conf -eq 1 ]; then
			echo ""
			echo  "\e[1;34m 2) Wi-Fi 연결 테스트 \e[0m"
			if ifconfig wlan0|grep "inet"> /dev/null; then 
				if ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null; then 
					echo  "  > Wi-Fi 연결이 있습니다";
					ping -q -w 1 -c 1 www.nist.org > /dev/null && echo "  > 외부 서버연결에 성공하였습니다."|| echo "  > 외부 서버연결에 실패하였습니다."
					echo "  > 엔터키를 누르면 메인 메뉴로 돌아갑니다."
					read choice; 
					case "$choice" in 
						*) 
							;; 
					esac
				else
					echo "  > Wi-Fi가 정상적으로 연결되어 있지 않습니다";
					echo "  > Wi-FI 연결 및 IP 설정을 확인해 주세요";
					echo "  > 엔터키를 누르면 메인 메뉴로 돌아갑니다."
					read choice; 
					case "$choice" in 
						*) 
						;;
					esac
				fi
			else 
				echo "  > Wi-Fi가 정상적으로 연결되어 있지 않습니다";
				echo "  > Wi-FI 연결 및 IP 설정을  확인해 주세요";
				echo "  > 엔터키를 누르면 메인 메뉴로 돌아갑니다."
				read choice; 
				case "$choice" in 
					*) 
					;;
				esac
			fi
		fi
		#read out
		;;
	[4]*)
		echo ""
		echo  "\e[1;34m인터넷 속도 테스트 진행합니다. \e[0m"
		#echo ""
		speedtest-cli
		echo ""
		echo  "\e[1;34m다운로드 속도가 5Mbps 이하인 경우에는 지니블록 진행이 다소 느릴 수 있습니다.\e[0m"
		echo ""
		echo "> 엔터키를 누르면 메인 메뉴로 돌아갑니다."
		read out
		;;
		
	[5]*)
		echo ""
		echo  "AMK 사전 환경 프로그램을 종료합니다.\n감사합니다."
		echo ""
		break
		exit;;
	esac
done
