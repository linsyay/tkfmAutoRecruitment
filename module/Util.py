import re
from hangul_utils import split_syllables, join_jamos
from symspellpy import SymSpell, Verbosity

def RegexToKor(tag_list):
    out = []
    for tag in tag_list:
        results = re.compile('[가-힣]').findall(tag)
        out_tag = ''
        for item in results:
            out_tag += item
        out.append(out_tag)
    return out

def findSimilarity(char):
    sym_spell = SymSpell(max_dictionary_edit_distance=3)
    dicionary_path = "data\\tags_dictionary.txt"
    sym_spell.load_dictionary(dicionary_path, 0, 1, encoding='utf-8')
    
    term = split_syllables(char)

    suggestions = sym_spell.lookup(term, Verbosity.ALL, max_edit_distance=3)

    # for sugg in suggestions:
    #     print(sugg.term, join_jamos(sugg.term), sugg.distance, sugg.count)
    return join_jamos(suggestions[0].term)