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

bp.route("/cards", methods=["POST"])
# 로그인 상태 데코레이터함수 넣기
# 로그인 상태함수 내부에는 엑세스토큰 확인하고 user_id 꺼내서 사용
def card_post():

    input_data = request.get_json()
    title = input_data.get("title")
    content = input_data.get("content")

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

