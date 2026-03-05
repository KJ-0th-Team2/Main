# ObjdectId 직렬화 
def serialize_id(data):
    if isinstance(data,list):
        for item in data:
            item["_id"] = str(item["id"])
    else:
        data["_id"] = str(data["_id"])
    return data