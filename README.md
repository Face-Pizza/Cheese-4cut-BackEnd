# 치즈네컷
2024 멋쟁이사자처럼 중앙 해커톤 얼굴피자 팀 <br/>
2024.07.11 ~

## 주요 모듈
- Django (웹서버)
- Pillow (이미지 처리)
- qrcode (QR코드 생성)
- pywin32 (프린터 제어)

## 코드 흐름
### 클라이언트
1. 사진 유형 선택 `Home.jsx`
- 표정 챌린지 네컷 (목표 표정이 인식되면 사진이 찍힘)
- 내맘대로 표정 네컷 (현재 표정을 실시간 인식해서 텍스트로 표시)<br/>

2. 프린트 매수 선택 `PaymentPage.jsx`
- 프린트 할 매수를 두 장 단위로 선택<br/>

3. 사진 촬영 `ShootPage.jsx`
- 우리의 메인 기능인 표정 인식 기능이 들어 있는 페이지
- `face-api.js`를 사용해 현재 표정을 인식 (`useEmotionDetection.js`에서 api 관리)
    - 0.25초 간격으로 표정 인식
    - 인식된 감정들 중 max 값을 찾아 `maxExpression`과 확률 `confidence`를 반환<br/>

4. 사진 선택 `SelectionPage.jsx`
- 8컷의 사진 중 4장 선택
- 프레임 변경
- 프린트하기 버튼을 누름과 동시에 django 서버에 사진 저장<br/>

5. 프린트 페이지 `PrintPage.jsx`
- 프린트 중이라는 안내 문구 띄우기
- `timer`가 0이 되면 다시 메인 페이지 `Home.jsx`로 이동<br/>

### 클라이언트-서버
1. react에서 django로 사진 전송
- 사진을 image 형식으로 post<br/>

2. QRcode 생성
- db에 photo가 저장되면서 동시에 qrcode 생성 `views.py`
    - qrcode 생성 코드는 `utils.py`로 분리해서 관리함
- 로컬 react에서 사진을 찍고, django 서버로 전송, django 서버는 네컷 사진을 다운받을 수 있는 배포된 react랑 다시 연결<br/>

3. 네컷 사진에 qrcode 출력
- react에서 qr_code를 get 해서 불러옴
- 해당 qrcode를 찍으면 사진을 다운받을 수 있는 링크로 연결<br/>

4. 프린터기 (`views.py`에서 관리)
- react에서 django로 post로 받은 파일을 임시 저장, 프린터로 전송 `print_file`
- 프린터 정보를 가져와 image file을 프린터의 해상도에 맞게 조정 후 출력 `print_image`
    - 프린터기 연동 `hDC.StartDoc()` `hDC.StartPage`<br/>

5. 사진 다운로드
- django 서버에서 photo를 get 해오기
- 사진 다운로드 기능 제공


## 프론트 세팅
설치 필요한 라이브러리 <br/>
<br/>
```commandline
npm i
npm install react-router-dom
npm install styled-components
```

## 백엔드 세팅
1. 가상환경 생성
```commandline
python -m venv venv
source venv/Scripts/activate
```
2. 필요 모듈 설치
```commandline
pip install django
pip install djangorestframework
pip install Pillow
pip install qrcode
pip install django-cors-headers
pip install pywin32
```
3. 실행
```commandline
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```