import os, json

from itertools import combinations
from module import Util

def FindTagNumToKor(tag_list):
    rootDir = os.path.dirname(__file__)
    korInfoDir = os.path.join(rootDir, '..\data\KorInfo.json')
    with open(korInfoDir, 'r', encoding="utf-8") as f:
        korInfoJson = json.load(f)
    out = []
    for tag in tag_list:
        out.append(korInfoJson.get("tags").index(tag))
    return out

def FindListAll(tags_num):
    rootDir = os.path.dirname(__file__)
    characterTagDir = os.path.join(rootDir, '..\data\CharacterTag.json')
    with open(characterTagDir, 'r', encoding="utf-8") as f:
        characterTagJson = json.load(f)
    out = []
    for tag in tags_num:
        out += characterTagJson.get(str(tag))
    cleanOut = sorted(list(set(out)))

    return cleanOut

def FindCharacter(tags_num):
    cleanList = FindListAll(tags_num)
    
    if 20 in cleanList:
        tagSummonCharacterList = GetTagSummonCharacterSSR(tags_num, cleanList)
    else:
        tagSummonCharacterList = GetTagSummonCharacterNonTag(tags_num, cleanList)
        td = GetTreeDictionaryNonTag(tagSummonCharacterList)
        
    return td

def GetTagSummonCharacterSSR(tags_num, cleanList):
    rootDir = os.path.dirname(__file__)
    characterInfoDir = os.path.join(rootDir, '..\data\CharacterInfo.json')
    with open(characterInfoDir, 'r', encoding="utf-8") as f:
        characterInfoJson = json.load(f)
    return

def GetTagSummonCharacterNonTag(tags_num, cleanList):
    rootDir = os.path.dirname(__file__)
    characterInfoDir = os.path.join(rootDir, '..\data\CharacterInfo.json')
    with open(characterInfoDir, 'r', encoding="utf-8") as f:
        characterInfoJson = json.load(f)
    nonSSRList = list(map(str, list(filter(Util.nonSSRCharacter, list(map(int, cleanList))))))
    
    out = []
    for character in nonSSRList:
        for characterInfo in characterInfoJson:
            if characterInfo.get("id") == str(character):
                tagList = characterInfo.get("tags")
        intersectionList = list(set(tags_num).intersection(tagList))
        intersectionList.sort()
        out.append({"id" : str(character), "tags" : intersectionList})

    return out

def GetTreeDictionaryNonTag(tagSummonCharacterList):
    out = {"DefinitiveSSR" : [], "DefinitiveSR" : [], "DefinitiveCharacter" : [], "Default" : []}
    
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
                print(tagLen)
            for dcTag in dc.get("tags"):
                if (len(dcTag) > tagLen):
                    dc.get("tags").remove(dcTag)
    
    for dc in out["DefinitiveCharacter"]:
        tagLen = 5
        if len(dc.get("tags")) > 1:
            for dcTag in dc.get("tags"):
                tagLen = min(tagLen, len(dcTag))
                print(tagLen)
            for dcTag in dc.get("tags"):
                if (len(dcTag) > tagLen):
                    dc.get("tags").remove(dcTag)
    
    out["Default"] = tagSummonCharacterList
    print(out)
    return out