from bson import ObjectId
import re

# ObjdectId 직렬화 
def serialize_id(data):
    if not data:
        return data
    
    if isinstance(data,list):
        for item in data:
            if "_id" in item:
                item["_id"] = str(item["_id"])
    else:
        if "_id" in data:
            data["_id"] = str(data["_id"])
    return data

# ObjectId로 변환
def to_object_id(id):
    try:
        return ObjectId(id)
    except: return None

def strip_markdown(text):
    text = re.sub(r'<br\s*/?>', '', text)
    text = re.sub(r'[*_~`#><]', '', text)  # 기호 제거
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # 링크 제거
    return text.strip()