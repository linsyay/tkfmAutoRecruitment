import os, json

from itertools import combinations

FILTER_NONE_SSR = 1
FILTER_SSR = 2

# 추출한 한글 태그 정보를 숫자 태그 정보로 변환 (main/WindowClass/ScanAutoFiltering)
def FindTagNumToKor(tag_list):
    rootDir = os.path.dirname(__file__)
    korInfoDir = os.path.join(rootDir, '..\\data\\KorInfo.json')
    with open(korInfoDir, 'r', encoding="utf-8") as f:
        korInfoJson = json.load(f)
    out = []
    for tag in tag_list:
        out.append(korInfoJson.get("tags").index(tag))
    return out

# 추출한 태그를 바탕으로 가능한 캐릭터 리스트 전부 추출
def FindListAll(tags_num, filter):
    rootDir = os.path.dirname(__file__)
    characterTagDir = os.path.join(rootDir, '..\\data\\CharacterTag.json')
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
        td = GetTreeDictionarySSRTag(tagSummonCharacterList)
    else: # 리더 태그가 없을 경우
        tagSummonCharacterList = GetTagSummonCharacter(tags_num, FILTER_NONE_SSR)
        td = GetTreeDictionaryNonTag(tagSummonCharacterList)

    return td

# 캐릭터와 태그의 Dictionary List 추출
def GetTagSummonCharacter(tags_num, filter):
    # 부분집합 떄문에 강제 설정한 태그 지워야함
    # tags_num = [3, 4, 8, 9, 17]
    
    cleanList = list(FindListAll(tags_num, filter)) # 추출한 태그를 바탕으로 가능한 캐릭터 리스트 전부 추출
    
    rootDir = os.path.dirname(__file__)
    characterInfoDir = os.path.join(rootDir, '..\\data\\CharacterInfo.json')
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

# 리더 태그가 없을 경우 (Tree Data)
def GetTreeDictionaryNonTag(tagSummonCharacterList):
    out = {"DefinitiveSSR" : [], "DefinitiveSR" : [], "DefinitiveCharacter" : [], "Default" : []}
    
    # SR 확정식 검색을 위해 SR를 따로 분리 (SplitTagSummonCharacterList)
    SplitTSCL = {"SR" : [], "NR" : []}
    for tsc in tagSummonCharacterList:
        if (int(tsc.get("id")) < 300):
            SplitTSCL["SR"].append(tsc)
        elif (int(tsc.get("id")) >= 300):
            SplitTSCL["NR"].append(tsc)

    subsets = []
    
    # SR 확정식 검색을 위해 SR List를 하나씩 돌아가면서 NR과 겹치지 않는지 확인
    for tsc_sr in SplitTSCL.get("SR"):
        # SR 캐릭터의 태그의 부분집합을 구함
        tsc_sr_subsets = list(combinations(tsc_sr.get("tags"), 1)) + list(combinations(tsc_sr.get("tags"), 2)) + list(combinations(tsc_sr.get("tags"), 3))
        
        # NR 캐릭터의 태그의 부분집합을 하나씩 돌아가면서 구함
        for tsc_nr in SplitTSCL.get("NR"):
            # 부분집합 구하기
            tsc_nr_subsets = list(combinations(tsc_nr.get("tags"), 1)) + list(combinations(tsc_nr.get("tags"), 2)) + list(combinations(tsc_nr.get("tags"), 3))
            # 차집합이 존재하는지 확인
            tsc_sr_subsets = list(set(tsc_sr_subsets).difference(tsc_nr_subsets))
        
        # 차집합이 존재한다면 SR 확정식으로 간주하여 subsets 리스트에 추가함
        if len(tsc_sr_subsets) > 0:
            subsets.append({"id" : tsc_sr.get("id"), "tags" : tsc_sr_subsets})
            
    print(subsets)
    
    # 확정식을 넣어 둔 subsets 리스트를 하나씩 돌아가면서 확정 SR식인지 확정 캐릭터식인지 체크
    for item_main in subsets:
        overlapSubset = False
        for tags in item_main.get("tags"):
            for item_sub in subsets:
                if item_main != item_sub:
                    if len(list(set([tags, ]).intersection(item_sub.get("tags")))) > 0:
                        out["DefinitiveSR"].append({"id" : item_main.get("id"), "tags" : [tags]})
                        overlapSubset = True
                        break
            if overlapSubset is False:
                out["DefinitiveCharacter"].append({"id" : item_main.get("id"), "tags" : [tags]})
    
    out["Default"] = tagSummonCharacterList
    print(out)
    return out

# 리더 태그가 있을 경우 (Tree Data)
def GetTreeDictionarySSRTag(tagSummonCharacterList):
    out = {"DefinitiveSSR" : [], "DefinitiveSR" : [], "DefinitiveCharacter" : [], "Default" : []}
    
    # SR 확정식 검색을 위해 SR를 따로 분리, SSR 리스트도 따로 분리 (SplitTagSummonCharacterList)
    SplitTSCL = {"SSR" : [], "SR" : [], "NR" : []}
    for tsc in tagSummonCharacterList:
        if (int(tsc.get("id")) < 200):
            SplitTSCL["SSR"].append(tsc)
        if (int(tsc.get("id")) >= 200) and (int(tsc.get("id")) < 300):
            SplitTSCL["SR"].append(tsc)
        elif (int(tsc.get("id")) >= 300):
            SplitTSCL["NR"].append(tsc)

    subsets = []
    
    # SR 확정식 검색을 위해 SR List를 하나씩 돌아가면서 NR과 겹치지 않는지 확인
    for tsc_sr in SplitTSCL.get("SR"):
        # SR 캐릭터의 태그의 부분집합을 구함
        tsc_sr_subsets = list(combinations(tsc_sr.get("tags"), 1)) + list(combinations(tsc_sr.get("tags"), 2)) + list(combinations(tsc_sr.get("tags"), 3))
        
        # NR 캐릭터의 태그의 부분집합을 하나씩 돌아가면서 구함
        for tsc_nr in SplitTSCL.get("NR"):
            # 부분집합 구하기
            tsc_nr_subsets = list(combinations(tsc_nr.get("tags"), 1)) + list(combinations(tsc_nr.get("tags"), 2)) + list(combinations(tsc_nr.get("tags"), 3))
            # 차집합이 존재하는지 확인
            tsc_sr_subsets = list(set(tsc_sr_subsets).difference(tsc_nr_subsets))
        
        # 차집합이 존재한다면 SR 확정식으로 간주하여 subsets 리스트에 추가함
        if len(tsc_sr_subsets) > 0:
            subsets.append({"id" : tsc_sr.get("id"), "tags" : tsc_sr_subsets})
    
    # 확정식을 넣어 둔 subsets 리스트를 하나씩 돌아가면서 확정 SR식인지 확정 캐릭터식인지 체크
    for item_main in subsets:
        overlapSubset = False
        for tags in item_main.get("tags"):
            for item_sub in subsets:
                if item_main != item_sub:
                    if len(list(set([tags, ]).intersection(item_sub.get("tags")))) > 0:
                        out["DefinitiveSR"].append({"id" : item_main.get("id"), "tags" : [tags]})
                        overlapSubset = True
                        break
            if overlapSubset is False:
                out["DefinitiveCharacter"].append({"id" : item_main.get("id"), "tags" : [tags]})
    
    subsets.clear()
    
    # SSR 확정식 체크
    for tsc_ssr_main in SplitTSCL.get("SSR"):
        tsc_ssr_main_subsets = list(combinations(tsc_ssr_main.get("tags"), 1)) + list(combinations(tsc_ssr_main.get("tags"), 2)) + list(combinations(tsc_ssr_main.get("tags"), 3))
        
        for tsc_ssr_sub in SplitTSCL.get("SSR"):
            if tsc_ssr_main != tsc_ssr_sub:
                # 부분집합 구하기
                tsc_ssr_sub_subsets = list(combinations(tsc_ssr_sub.get("tags"), 1)) + list(combinations(tsc_ssr_sub.get("tags"), 2)) + list(combinations(tsc_ssr_sub.get("tags"), 3))
                # 차집합이 존재하는지 확인
                tsc_ssr_main_subsets = list(set(tsc_ssr_main_subsets).difference(tsc_ssr_sub_subsets))
        
        # 차집합이 존재한다면 SSR 확정식으로 간주하여 subsets 리스트에 추가함
        for item in tsc_ssr_main_subsets:
            if 20 in item:
                subsets.append({"id" : tsc_ssr_main.get("id"), "tags" : [item]})
        
    out["DefinitiveSSR"] = subsets

    out["Default"] = tagSummonCharacterList
    return out