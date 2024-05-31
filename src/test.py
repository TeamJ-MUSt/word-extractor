

import re

s = '(체언(体言)＋‘の’ ‘が’, 또는 용언(用言)[주로 동사, 또는 거기에 조동사가 붙은 것]의 연체형(連体形), 또는, 그것에 ‘が’가 붙은 꼴에 이어져서) 그 사항이 다음에 말하는 것의 목적임을 나타내는 말: 위함.'
def contains_korean(text):
    # Regular expression to match Korean characters
    korean_pattern = re.compile("[ㄱ-힣]+")
    return bool(korean_pattern.search(text))

def has_japanese_characters(text):
    japanese_pattern = re.compile('[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]+')
    return bool(japanese_pattern.search(text))

def pred(text):
    if len(text) == 0 or len(text) > 5 or has_japanese_characters(text) or not contains_korean(text):
        return True
    return False

print(remove_parentheses_content(s, pred))