# AI Makers Kit(AI Coding Pack) 3rd Party 공식 개발 사이트

## 지니블럭 3rd Robot 연동 개발 절차
### Step.1 지니블록과 3rd Toy Robot 연동하기 위한 사전 준비 (수신 이메일: amkeco7@gmail.com)
- 지니블럭에서 구현하려는 Robot의 기능에 대한 API 정의
- 지니블럭에서 사용하려는 블럭에 대한 규격 정의
  .Google Docs 스프레드시트로 규격 공유 (수신 이메일로 요청)
  ![curcuit](https://github.com/amk-eco/official/blob/master/img/robot_api.png)

- 블럭 디자인 샘플(시안) 정의

-> 위에서 언급한 사항이 모두 완료 시 Step2 진행

### Step.2 지니블록 테스트 서버에 요구사항 반영
- Step1 에서 요청한 사항에 대해서 지니블록 테스트 서버에 반영
- 반영 완료 후, 테스트 서버 URL 제공

### Step.3 AMK 단말 Client 개발(BlcokDriver.js)
- 테스트 서버용 AMK Client 지니블럭 드라이버 제공 (3rd Party Robot 전용 github 사이트를 생성 후 업로드)
- 해당 지니블럭 블록 드라이버의 BlockDriver.js 파일에서 지니블럭 서버에서 전송하는 메세지를 처리할 NodeJS 코드를 작성
- BlockDriver.js과 연동되는(Call 할 수 있는) Robot API 라이브러리를 개발 (Robot이 BLE 통신을 할 경우, Python 언어를 통해 개발하는 것이 원칙)
- AMK 단말에서 운용할 Robot의 Client 개발이 완료될 경우, 제공한 github 사이트를 통해 업로드(commit)

### Step.4 AMK 단말 내에서 Robot 연동 테스트
- AMK 단말에서 지니블럭과 Robot의 연동이 정상적으로 이루어지는 확인

### Step.5 상용 서버 및 공식 OS 반영 요청
- 요청 시 검증 후 상용 서버 반영
- AMK 공식 OS 및 업데이트에 반영하여 배포 

## 기타 문의 및 요청
- amkeco7@gmail.com 메일로 송신 바람
