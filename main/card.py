from flask import render_template, Blueprint, request, jsonify
from db import db
from datetime import datetime
from utils import serialize_id
from utils import to_object_id

bp = Blueprint('card',__name__)

@bp.route("/api/cards", methods=["GET"])
#페이지 네이션 적용
def get_cards():
    sort_param = request.args.get("sort","latest")
    SORT_MAP ={
        "latest": ("created_at", -1),
        "views": ("view_count",-1),
        "comments" :("comment_count", -1)
    }
    field, order = SORT_MAP.get(sort_param, ("created_at", -1))
    try:
        cards = list(db.card.find({}).sort(field, order))
        # return jsonify({"result": "success", "data": serialize_id(cards)}), 200
        # jinja2
        return render_template("cards.html", cards=serialize_id(cards)),200
    except Exception as e:
        print(e)
        #return jsonify({"result": "fail", "msg": "서버 오류"}), 500
        # jinja2
        return render_template("error.html", msg="서버 오류"), 500

@bp.route("/api/cards", methods=["POST"])
# 로그인 상태 데코레이터함수 넣기
# 로그인 상태함수 내부에는 엑세스토큰 확인하고 user_id 꺼내서 사용
def card_post():

    input_data = request.get_json()
    title = input_data.get("title")
    content = input_data.get("content")
    print(title, content)

    if not title or not content:
        return jsonify({"result":"fail", "msg":"제목과 내용은 필수 항목입니다."}), 400
    

    card={
        "title":title,
        "content":content,
        "version":1,
        "created_at": datetime.now(),
        "comment_count":0,
        # "projects":[]
        # "author":user_id
    }

    try: 
        result = db.card.insert_one(card)
        return jsonify({"result":"sucess", "msg":"등록이 완료되었습니다."}),200
    
    except Exception as e:
        print(e)
        return jsonify({"result":"fail", "msg":"등록 실패하였습니다."}),500

@bp.route("/api/cards/search", methods=["GET"])
def search_card():

    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify({"result":"fail", "msg":"검색어를 입력해주세요"}), 401
    try:
        find_cards = list(db.card.find({"title":{"$regex":keyword, "#options": "i"} },{"_id":1, "title":1}))
      

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
    
