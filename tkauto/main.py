import os, sys, json

# PyQT Module
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

# PyQt Design Library
from qt_material import QtStyleTools

# 분리된 Module Import
import Capture, ImgProcessing, Util, FindCharacterByTag

# Qt Designer로 만든 UI 불러오기
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
form_class = uic.loadUiType(BASE_DIR + r"\\tkfm_UI.ui")[0]

# 실행중인 Process List
global win_list
# 처음 실행됬을 때 None으로 초기화
win_list = None

class WindowClass(QMainWindow, QtStyleTools, form_class):
    # 초기화 함수
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_style()
        
        # 프로세스 찾기 버튼을 클릭하면 ScanProcessList 함수를 호출하는 이벤트 연결
        self.ScanWindow.clicked.connect(self.ScanProcessList)
        # 스캔 버튼을 클릭하면 ScanAutoFiltering 함수를 호출하는 이벤트 연결
        self.ScanButton.clicked.connect(self.ScanAutoFiltering)
        
    # QT-Material Style
    def set_style(self):
        extra = {}
        extra['font_family'] = 'Roboto'
        extra['density_scale'] = str(-1)
        
        # invert : Light themes (True is Light, False is Dark)
        self.apply_stylesheet(self, theme='dark_pink.xml', extra=extra, invert_secondary=False)
        
        # 스캔 결과 Column의 Width 크기 (마지막 Column은 자동)
        self.treeWidget.setColumnWidth(0, 180)
        self.treeWidget.setColumnWidth(1, 80)
        
    # 현재 실행중인 프로세스의 리스트를 검색하는 함수
    def ScanProcessList(self):
        global win_list
        win_list = Capture.get_win_list()
        self.ProcessListBox.clear()
        for win_item in win_list:
            self.ProcessListBox.addItem(win_item[0]) # 프로세스 드롭다운 박스에 추가
    
    # 스캔 버튼을 클릭했을 때 실행되는 함수
    def ScanAutoFiltering(self):
        try:
            # ProcessList Dropdown Box에 현재 Index를 가져옴
            hwnd = win_list[self.ProcessListBox.currentIndex()][1]
            
            # 선택된 Process의 좌, 상, 우, 하의 크기를 가져옴
            x1, y1, x2, y2 = Capture.get_win_size(hwnd)
            
            # 가져온 이미지 정보를 바탕으로 이미지를 촬영함
            Capture.get_win_image(x1, y1, x2, y2)
            
            # 촬영된 스크린샷에서 태그 정보를 추출해서 tag_list 변수에 담음
            tag_list = Util.RegexToKor(ImgProcessing.RootImageTrim())
            
            # 태그 오류 수정 (최적화 필요)
            for index, item in enumerate(tag_list):
                tag_list[index] = Util.findSimilarity(item)
            
            print("추출된 태그 : ", tag_list)
            
            # 추출한 한글 태그 정보를 숫자 태그 정보로 변환
            tags_num = FindCharacterByTag.FindTagNumToKor(tag_list)
            tags_num.sort()
            
            # 추출된 태그 리스트들을 프로그램 상에 체크 표시 (ScanAutoButton 함수 호출) (좌 하단 영역)
            self.ScanAutoButton(tags_num)
            
            # 추출한 태그 정보를 바탕으로 캐릭터 리스트 조회
            tagSummonCharacterList = FindCharacterByTag.FindCharacter(tags_num)
            
            # 완성된 Tree Data를 바탕으로 Tree Widget으로 출력
            self.SetTreeWidget(tagSummonCharacterList)
        except:
            QMessageBox.warning(self, 'Warning', '스캔 과정에서 오류가 발생하였습니다')

    # 완성된 Tree Data를 바탕으로 Tree Widget으로 출력
    def SetTreeWidget(self, tagSummonCharacterList):
        rootDir = os.path.dirname(__file__)
        korInfoDir = os.path.join(rootDir, 'data\\KorInfo.json')
        with open(korInfoDir, 'r', encoding="utf-8") as f:
            korInfoJson = json.load(f)
        
        # 스캔 후 TreeWidget 재설정 (초기화)
        self.ClearTreeWidget()
        
        # SSR 확정 조합식
        if len(tagSummonCharacterList["DefinitiveSSR"]) > 0:
            for tsc in tagSummonCharacterList["DefinitiveSSR"]:
                treeZero = self.treeWidget.topLevelItem(0)
                itemZero = QTreeWidgetItem(treeZero)
                itemZero.setText(0, korInfoJson.get('name').get(tsc.get("id")))
                itemZero.setText(1, "⁂ SSR")
                out = ''
                for tags in tsc.get("tags"):
                    out += "["
                    for tag in tags:
                        out += korInfoJson.get('tags')[int(tag)]
                        out += ", "
                    out = out.rstrip(", ")
                    out += "], "
                out = out.rstrip(', ')
                itemZero.setText(2, out)
        
        # SR 확정 조합식
        if len(tagSummonCharacterList["DefinitiveSR"]) > 0:
            for tsc in tagSummonCharacterList["DefinitiveSR"]:
                treeOne = self.treeWidget.topLevelItem(1)
                itemOne = QTreeWidgetItem(treeOne)
                itemOne.setText(0, korInfoJson.get('name').get(tsc.get("id")))
                itemOne.setText(1, "⁑ SR")
                out = ''
                for tags in tsc.get("tags"):
                    out += "["
                    for tag in tags:
                        out += korInfoJson.get('tags')[int(tag)]
                        out += ", "
                    out = out.rstrip(", ")
                    out += "], "
                out = out.rstrip(', ')
                itemOne.setText(2, out)
                
        # SR 조합식
        if len(tagSummonCharacterList["DefinitiveCharacter"]) > 0:
            for tsc in tagSummonCharacterList["DefinitiveCharacter"]:
                treeTwo = self.treeWidget.topLevelItem(2)
                itemTwo = QTreeWidgetItem(treeTwo)
                itemTwo.setText(0, korInfoJson.get('name').get(tsc.get("id")))
                itemTwo.setText(1, "⁑ SR")
                out = ''
                for tags in tsc.get("tags"):
                    out += "["
                    for tag in tags:
                        out += korInfoJson.get('tags')[int(tag)] + ", "
                    out = out.rstrip(", ")
                    out += "], "
                out = out.rstrip(', ')
                itemTwo.setText(2, out)
        
        # 전체 조합식
        if len(tagSummonCharacterList["Default"]) > 0:
            for tsc in tagSummonCharacterList["Default"]:
                treeThree = self.treeWidget.topLevelItem(3)
                itemThree = QTreeWidgetItem(treeThree)
                itemThree.setText(0, korInfoJson.get('name').get(tsc.get("id")))
                
                if (int(tsc.get("id")) < 200):
                    itemThree.setText(1, "⁂ SSR")
                elif (int(tsc.get("id")) < 300):
                    itemThree.setText(1, "⁑ SR")
                elif (int(tsc.get("id")) < 400):
                    itemThree.setText(1, "⁎ R")
                elif (int(tsc.get("id")) < 500):
                    itemThree.setText(1, "N")
                out = ''
                for tag in tsc.get("tags"):
                    out += korInfoJson.get('tags')[int(tag)] + ", "
                out = out.rstrip(", ")
                itemThree.setText(2, out)
                
            
    # 스캔 후 Tag 변수 리스트화 및 자동 체크
    def ScanAutoButton(self, tags_num):
        tagButtonList = [self.TagBtn00, self.TagBtn01, self.TagBtn02, self.TagBtn03, self.TagBtn04, self.TagBtn05, self.TagBtn06, self.TagBtn07, self.TagBtn08, self.TagBtn09, self.TagBtn10,
                         self.TagBtn11, self.TagBtn12, self.TagBtn13, self.TagBtn14, self.TagBtn15, self.TagBtn16, self.TagBtn17, self.TagBtn18, self.TagBtn19, self.TagBtn20,
                         self.TagBtn21, self.TagBtn22, self.TagBtn23, self.TagBtn24, self.TagBtn25, self.TagBtn26, self.TagBtn27, self.TagBtn28, self.TagBtn29, self.TagBtn30,
                         self.TagBtn31, self.TagBtn32]
        
        # 기존 체크되있는 리스트 제거
        for index in range(0, 33):
            tagButtonList[index].setCheckState(0)
            
        # 현재 태그 정보로 갱신
        for tag in tags_num:
            tagButtonList[tag].setCheckState(2)
    
    # 스캔 후 TreeWidget 재설정 (초기화)
    def ClearTreeWidget(self):
        treeWidgetTextList = ["[⁂SSR] 확정 조합식", "[⁑SR] 확정 조합식", "[⁑SR] 조합식", "[전체] 조합식"]
        self.treeWidget.clear()
        
        for index in range(0, 4):
            item = QTreeWidgetItem()
            item.setText(0, treeWidgetTextList[index])
            self.treeWidget.invisibleRootItem().addChild(item)
    
    
if __name__ == '__main__':
   app = QApplication(sys.argv)
   myWindow = WindowClass()
   myWindow.show()
   app.exec_()