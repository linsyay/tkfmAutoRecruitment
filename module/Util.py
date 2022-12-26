import re
import os, json
from difflib import get_close_matches

from module import FindCharacterByTag

def RegexToKor(tag_list):
    out = []
    for tag in tag_list:
        results = re.compile('[가-힣]').findall(tag)
        out_tag = ''
        for item in results:
            out_tag += item
        out.append(out_tag)
    return out

def findSimilarity():
    
    return True

def nonSSRCharacter(numList):
    return numList>200

def FindSRCharacter(tagSummonCharacterList):
    out = {"SR" : [], "NR" : []}
    for tsc in tagSummonCharacterList:
        if (int(tsc.get("id")) < 300):
            out["SR"].append(tsc)
        elif (int(tsc.get("id")) > 300):
            out["NR"].append(tsc)
    return out