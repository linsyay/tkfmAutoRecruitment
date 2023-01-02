import cv2
# print(cv2.__file__)

import TesseractOCR

def RootImageTrim():
    img = cv2.imread('screenshot.png')
    output = []
    for index in range(0, 5):
        output.append(ImageTrim(img, index))
    return output

def ImageTrim(img, index):
    # Image의 Root 크기
    rh, rw, rc = img.shape
    
    # 모집 조건 위치 잡기 코드
    x = int(rw/6); y = int(rh/2.58); w = int(rw/5.5); h = int(rh/30)
    
    img_trim = img[y+((index//3)*int(rh/18)) : y+((index//3)*int(rh/18))+h, x+(index%3)*int(rw/4.1) : x + (index % 3) * int(rw/4.1) + w]
    img_text = TesseractOCR.get_tag(img_trim)
    
    # 위치 테스트용 코드
    # cv2.imshow("img", img_trim)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return img_text