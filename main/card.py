from flask import render_template, Blueprint, request, jsonify
from pymongo import MongoClient
from datetime import datetime


client = MongoClient('localhost', 27017)
db = client.jungle_wiki
bp = Blueprint('card',__name__)

@bp.route("/cards", methods=["GET"])
def get_cards():
    sort_pram = request.args.get("sort","latest")
    SORT_MAP ={
        "latest": ("created_at", -1),
        "views": ("view_count",-1),
        "comments" :("comment_count", -1)
    }
    field, order = SORT_MAP.get(sort_pram, ("created_at", -1))
    cards = list(db.jungle_wiki.find({}).sort(field, order))
    return jsonify(cards)

@bp.route("/cards", methods=["POST"])
# 로그인 상태 데코레이터함수 넣기
# 로그인 상태함수 내부에는 엑세스토큰 확인하고 user_id 꺼내서 사용
def card_post():

    input_data = request.get_json()
    title = input_data.get("title")
    content = input_data.get("content")

    if not title or not content:
        return jsonify({"result":"fail", "msg":"제목과 내용은 필수 항목입니다."}), 400
    
    card={
        "title":title,
        "content":content,
        "version":1,
        "created_at": datetime.now()
        # "author":user_id
    }

    result = db.jungle_wiki.insert_one(card)
    try: 
        result.inserted_id
        return jsonify({"result":"sucess", "msg":"등록이 완료되었습니다."}),200
    
    except Exception as e:
        print(e)
        return jsonify({"result":"fail", "msg":"등록 실패하였습니다."}),500

@db.route("/cards/search", methods=["GET"])
def search_card():

    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify({"result":"fail", "msg":"검색어를 입력해주세요"}), 401
    try:
        find_cards = list(db.jungle_wiki.find({"title":{"$regex":keyword, "#options": "i"} },{"_id":1, "title":1}))
        for card in find_cards:
            # Objdctd는 JSON 직렬화 불가로 str변환 필요
            card["_id"] = str(card["_id"]) 

        if not find_cards:
            return jsonify({"result":"fail", "msg":"검색 결과가 없음"}), 404
        
        return jsonify({"result":"success", "msg":"해당카드 찾기 성공", "data":find_cards}), 200
    except:
        return jsonify({"result":"fail", "msg":"서버오류"}),500
        

 
