# from utils import serialize_id 
# serialize_id(직렬화할 값)

# ObjdectId 직렬화 
def serialize_id(data):
    if isinstance(data,list):
        for item in data:
            item["_id"] = str(item["_id"])
    else:
        data["_id"] = str(data["_id"])
    return data