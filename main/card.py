from flask import render_template, Blueprint, request, jsonify
from db import db
from bson import ObjectId
from datetime import datetime
from utils import to_object_id, serialize_id
from flask_jwt_extended import *

bp = Blueprint('card',__name__)

@bp.route("/api/cards", methods=["GET"])
def get_cards():
    sort_param = request.args.get("sort", "latest")
    page = int(request.args.get("page", 1))
    per_page = 9
    SORT_MAP = {
        "latest": ("created_at", -1),
        "oldest": ("created_at", 1),
    }
    field, order = SORT_MAP.get(sort_param, ("created_at", -1))
    try:
        pipeline = [
            {"$sort": {"version": -1}},
            {"$group": {
                "_id": "$title",
                "doc": {"$first": "$$ROOT"}
            }},
            {"$replaceRoot": {"newRoot": "$doc"}},
            {"$sort": {field: order}},
            {"$skip": (page - 1) * per_page},
            {"$limit": per_page},
        ]
        cards = list(db.card.aggregate(pipeline))
        print("카드 수:", len(cards))  # ← 추가
        for c in cards:
            print(c.get("title"), c.get("version"))  # ← 추가
        return render_template("cards.html", cards=serialize_id(cards)), 200
    except Exception as e:
        print("에러:", e)  # ← 에러 내용 확인
        return render_template("error.html", msg="서버 오류"), 500

# 로그인 상태 데코레이터함수 넣기
# 로그인 상태함수 내부에는 엑세스토큰 확인하고 user_id 꺼내서 사용
@bp.route("/api/cards", methods=["POST"])
@jwt_required()
def card_post():
    user_id = get_jwt_identity()
    input_data = request.get_json()
    title = input_data.get("title")
    content = input_data.get("content")

    if not title or not content:
        return jsonify({"result": "fail", "msg": "제목과 내용은 필수 항목입니다."}), 400

    # 같은 title 중 가장 높은 version 찾기
    existing = db.card.find_one({"title": title}, sort=[("version", -1)])
    next_version = existing["version"] + 1 if existing else 1

    card = {
        "title": title,
        "content": content,
        "version": next_version,
        "created_at": datetime.now(),
        "comment_count": 0,
        "author": user_id
    }

    try:
        db.card.insert_one(card)
        return jsonify({"result": "success", "msg": "등록이 완료되었습니다."}), 200
    except Exception as e:
        print(e)
        return jsonify({"result": "fail", "msg": "등록 실패하였습니다."}), 500

@bp.route("/api/cards/search", methods=["GET"])
def search_card():

    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify({"result":"fail", "msg":"검색어를 입력해주세요"}), 401
    try:
        find_cards = list(db.card.find({"title":{"$regex":keyword, "$options": "i"} },{"_id":1, "title":1}))
      

        if not find_cards:
            return jsonify({"result":"fail", "msg":"검색 결과가 없음"}), 404
        
        return jsonify({"result":"success", "msg":"해당카드 찾기 성공", "data":serialize_id(find_cards)}), 200
    except:
        return jsonify({"result":"fail", "msg":"서버오류"}),500
        

@bp.route("/api/cards/<cardId>", methods=["PATCH"])
def card_edit(cardId):

    input_data = request.get_json()
    title = input_data.get("title")
    content = input_data.get("content")

    try:
        if not title or not content:
            return jsonify({"result":"fail","msg":"제목과 내용은 필수입니다."}),400
        
        find_edit = db.card.find_one({"_id":to_object_id(cardId)})
    
        obj_id = to_object_id(cardId)

        if not obj_id:
            return jsonify({"result":"fail","msg":"잘못된 id"}),400
    
        find_edit = db.card.find_one({"_id": obj_id})
        if not find_edit:
            return jsonify({"result":"fail","msg":"해당 카드 없음"}),404
        
        if title == find_edit.get("title") and content == find_edit.get("content"):
            return jsonify({"result":"fail", "msg":"변경된 내용이 없습니다."}), 400

        result = db.card.update_one({"_id": obj_id},{"$set":{"title": title,"content": content}, "$inc":{ "version":1 }})
        if result.matched_count == 1:
            return jsonify({"result":"success", "msg":"수정 완료"}),200
        else:
            return jsonify({"result":"fail", "msg":"수정 실패"}), 500
    except Exception as e: 
        print(e)
        return jsonify({ "result":"fail", "msg":"서버오류"}), 500
    

@bp.route("/api/cards/<cardId>", methods=["GET"])
def card_detail(cardId):
    try:
        obj_id = to_object_id(cardId)
        if not obj_id:
            return jsonify({"result":"fail","msg":"잘못된 id"}), 400
        find_card = db.card.find_one({"_id": obj_id})
        if not find_card:
            return jsonify({"result":"fail","msg":"해당 카드 없음"}), 404
        find_card = serialize_id(find_card)
        return jsonify({"result":"success", "msg":"해당 상세페이지 찾음", "data": find_card}), 200
    except Exception as e:
        print(e)
        return jsonify({ "result":"fail", "msg":"서버오류"}), 500