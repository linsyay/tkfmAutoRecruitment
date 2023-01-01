import os, json

from itertools import combinations
from module import Util

FILTER_NONE_SSR = 1
FILTER_SSR = 2

# 추출한 한글 태그 정보를 숫자 태그 정보로 변환 (main/WindowClass/ScanAutoFiltering)
def FindTagNumToKor(tag_list):
    rootDir = os.path.dirname(__file__)
    korInfoDir = os.path.join(rootDir, '..\data\KorInfo.json')
    with open(korInfoDir, 'r', encoding="utf-8") as f:
        korInfoJson = json.load(f)
    out = []
    for tag in tag_list:
        out.append(korInfoJson.get("tags").index(tag))
    return out

# 추출한 태그를 바탕으로 가능한 캐릭터 리스트 전부 추출
def FindListAll(tags_num, filter):
    rootDir = os.path.dirname(__file__)
    characterTagDir = os.path.join(rootDir, '..\data\CharacterTag.json')
    with open(characterTagDir, 'r', encoding="utf-8") as f:
        characterTagJson = json.load(f)
    
    out = []
    
    # Filter 조건으로 리더 태그가 있을 때만 SSR을 검색에 포함하도록 함
    if filter is FILTER_NONE_SSR:
        for tag in tags_num:
            out += characterTagJson.get(str(tag))
        cleanOut = sorted(list(set(out))) # set으로 중복 삭제
        cleanOut = [item for item in cleanOut if int(item) >= 200]
    elif filter is FILTER_SSR:
        for tag in tags_num:
            out += characterTagJson.get(str(tag))
        cleanOut = sorted(list(set(out))) # set으로 중복 삭제
    return cleanOut

# 추출한 태그 정보를 바탕으로 캐릭터 리스트 조회 (main/WindowClass/ScanAutoFiltering)
def FindCharacter(tags_num): # tags_num은 추출한 태그 5개
    # 리더, 정예 태그가 있는지로 분기
    if 20 in tags_num: # 리더 태그가 있을 경우
        tagSummonCharacterList = GetTagSummonCharacter(tags_num, FILTER_SSR)
        return
    else:
        tagSummonCharacterList = GetTagSummonCharacter(tags_num, FILTER_NONE_SSR)
        if 19 in tags_num: # 정예 태그가 있을 경우
            return
        else: # 정예 혹은 리더 태그가 없을 경우
            td = GetTreeDictionaryNonTag(tagSummonCharacterList)
        
    return td

def GetTagSummonCharacterSSR(tags_num):
    rootDir = os.path.dirname(__file__)
    characterInfoDir = os.path.join(rootDir, '..\data\CharacterInfo.json')
    with open(characterInfoDir, 'r', encoding="utf-8") as f:
        characterInfoJson = json.load(f)
    return

# 캐릭터와 태그의 Dictionary List 추출
def GetTagSummonCharacter(tags_num, filter):
    cleanList = list(FindListAll(tags_num, filter)) # 추출한 태그를 바탕으로 가능한 캐릭터 리스트 전부 추출
    
    rootDir = os.path.dirname(__file__)
    characterInfoDir = os.path.join(rootDir, '..\data\CharacterInfo.json')
    with open(characterInfoDir, 'r', encoding="utf-8") as f:
        characterInfoJson = json.load(f)

    out = []
    
    # 캐릭터와 태그의 Dictionary의 List
    # [ {id : ~, tags: [ ~ ] }, ... ]
    for character in cleanList:
        for characterInfo in characterInfoJson:
            if characterInfo.get("id") == str(character):
                tagList = characterInfo.get("tags")
        intersectionList = list(set(tags_num).intersection(tagList))
        intersectionList.sort()
        out.append({"id" : str(character), "tags" : intersectionList})

    return out

# 정예 혹은 리더 태그가 없을 경우 (Tree Data)
def GetTreeDictionaryNonTag(tagSummonCharacterList):
    out = {"DefinitiveSSR" : [], "DefinitiveSR" : [], "DefinitiveCharacter" : [], "Default" : []}
    
    print("tagSummonCharacterList", tagSummonCharacterList)
    
    # out = {"SR" : [], "NR" : []}
    # for tsc in tagSummonCharacterList:
    #     if (int(tsc.get("id")) < 300):
    #         out["SR"].append(tsc)
    #     elif (int(tsc.get("id")) > 300):
    #         out["NR"].append(tsc)
    # return out
    
    splitTSCL_SR = Util.FindSRCharacter(tagSummonCharacterList).get("SR")
    splitTSCL_NR = Util.FindSRCharacter(tagSummonCharacterList).get("NR")
    
    subsets = []
    for tsc_sr in splitTSCL_SR:
        tsc_sr_subsets = list(combinations(tsc_sr.get("tags"), 1)) + list(combinations(tsc_sr.get("tags"), 2)) + list(combinations(tsc_sr.get("tags"), 3))
        
        for tsc_nr in splitTSCL_NR:
            tsc_nr_subsets = list(combinations(tsc_nr.get("tags"), 1)) + list(combinations(tsc_nr.get("tags"), 2)) + list(combinations(tsc_nr.get("tags"), 3))
            
            tsc_sr_subsets = list(set(tsc_sr_subsets).difference(tsc_nr_subsets))
        
        if len(tsc_sr_subsets) > 0:
            subsets.append({"id" : tsc_sr.get("id"), "tags" : tsc_sr_subsets})
    
    for subset_main in subsets:
        overlapSubset = False
        for subset_sub in subsets:
            if subset_main != subset_sub:
                if len(list(set(subset_main.get("tags")).intersection(subset_sub.get("tags")))) > 0:
                    out["DefinitiveSR"].append(subset_main)
                    overlapSubset = True
                    break
        if overlapSubset is False:
            out["DefinitiveCharacter"].append(subset_main)
            
    # 태그가 여러개일 경우 태그 삭제 방지를 위해 가장 적은 개수의 태그만 남김
    for dc in out["DefinitiveSR"]:
        tagLen = 5
        if len(dc.get("tags")) > 1:
            for dcTag in dc.get("tags"):
                tagLen = min(tagLen, len(dcTag))
            for dcTag in dc.get("tags"):
                if (len(dcTag) > tagLen):
                    dc.get("tags").remove(dcTag)
    
    for dc in out["DefinitiveCharacter"]:
        tagLen = 5
        if len(dc.get("tags")) > 1:
            for dcTag in dc.get("tags"):
                tagLen = min(tagLen, len(dcTag))
            for dcTag in dc.get("tags"):
                if (len(dcTag) > tagLen):
                    dc.get("tags").remove(dcTag)
    
    out["Default"] = tagSummonCharacterList
    print(out)
    return out