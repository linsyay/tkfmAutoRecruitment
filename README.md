## tkfmAutoRecruitment

This can make TenkafuMA Recruitment automatically (Only Korean)

## 설치 방법
1. 파이썬 3.7.0 설치 (https://www.python.org/downloads/release/python-370/) 
    > Windows x86-64 executable installer를 선택해서 다운 (Window 기준)
    > 
    > Add Python 3.7 to PATH 체크박스를 반드시 선택     
    > 
    > 설치 경로를 기본 경로로 설정 (C 드라이브)
    > 
    > 모든 테스트는 3.7.0 환경에서 이루어졌음을 알림   
2. Tesseract-OCR 설치 (https://github.com/UB-Mannheim/tesseract/wiki)
    > Choose Components에서 Additional language data (download) - Korean 선택
    >
    > 설치 경로를 기본 경로로 설정 (C:\Program Files\Tesseract-OCR)  
    > (설치 경로가 달라진다면 tkauto의 pytesseract 경로 설정을 수정해야 함)   
3. CMD (명령 프롬프트) 실행
    > 파이썬 버전이 3.7.0으로 나오는지 확인
    > ```
    > python --version
    > ```
    > ![image](https://user-images.githubusercontent.com/85004072/210209859-551df53d-a60f-4734-b5ee-24feb35c4a55.png)
4. tkauto 파이썬 패키지 설치
    > CMD 안에서 명령어 실행
    > ```
    > python -m pip install tkauto
    > ```
    > ![image](https://user-images.githubusercontent.com/85004072/210209947-ba8ffb57-f12f-4a84-833b-ee96fc3b2e5a.png)
5. ( [본인의 파이썬 설치 경로] \ Lib \ site-packages \ tkauto ) 안의 main.py 실행
    > C:\Users\\[ 개인마다 다름 ]\AppData\Local\Programs\Python\Python37\Lib\site-packages\tkauto 경로로 이동
    >
    > 폴더 경로를 한번 클릭해서 전부 지운 다음 cmd를 입력
    >
    >![image](https://user-images.githubusercontent.com/85004072/210211678-42f36c76-12f4-4e2e-9a76-425d81652078.png)
    >
    > CMD (명령 프롬프트) 창에서 main.py 실행
    > ```
    > python main.py
    > ```
    >![image](https://user-images.githubusercontent.com/85004072/210210752-2cf58bd9-5572-4cd5-ae8e-f41541a1f31b.png)


## 라이브러리  

- PyQt5     
  https://www.riverbankcomputing.com/software/pyqt/intro

- Qt-Material    
  https://github.com/UN-GCPDS/qt-material

- TesseractOCR  
  https://github.com/tesseract-ocr/tesseract

- pytesseract  
  https://github.com/madmaze/pytesseract

- opencv  
  https://opencv.org/

- symspellpy  
  https://github.com/mammothb/symspellpy

- hangul_utils  
  https://github.com/kaniblu/hangul-utils

- Pillow  
  https://pillow.readthedocs.io/en/stable/

- win32gui  
  https://github.com/mhammond/pywin32
