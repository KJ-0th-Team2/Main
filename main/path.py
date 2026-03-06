from flask import render_template, Blueprint, request
from db import db
from utils import serialize_id, to_object_id, strip_markdown 

#
bp = Blueprint('path', __name__)



@bp.route('/detail/<cardId>')
def detail(cardId):
    obj_id = to_object_id(cardId)
    if not obj_id:
        return "잘못된 ID", 400
    
    find_card = db.card.find_one({"_id": obj_id})
    if not find_card:
        return "카드 없음", 404
    
    find_card = serialize_id(find_card)
    return render_template('detail.html', card=find_card)

@bp.route('/upload')
def upload():
    return render_template('upload.html')

@bp.route('/update')
def update():
    return render_template('update.html')

@bp.route('/history/<title>')
def history(title):
    histories = list(db.card.find({"title": title}).sort("version", -1))
    for h in histories:
        if h.get('created_at'):
            h['created_at'] = h['created_at'].strftime('%Y-%m-%d %H:%M')
    histories = serialize_id(histories)
    return render_template('history.html', histories=histories, title=title)

@bp.route("/")
def index():
    sort_param = request.args.get("sort", "latest")
    keyword = request.args.get("keyword", "") 
    
    SORT_MAP = {
        "latest": ("created_at", -1),
        "old": ("created_at", 1),
        "views": ("view_count", -1),
        "comments": ("comment_count", -1)
    }
    
    field, order = SORT_MAP.get(sort_param, SORT_MAP["latest"])

    try:
        match_stage = {"$match": {"title": {"$regex": keyword, "$options": "i"}}} if keyword else {"$match": {}}

        pipeline = [
            match_stage,
            {"$sort": {"version": -1}},
            {"$group": {
                "_id": "$title",
                "doc": {"$first": "$$ROOT"}
            }},
            {"$replaceRoot": {"newRoot": "$doc"}},
            {"$sort": {field: order}},
        ]

        cards_cursor = list(db.card.aggregate(pipeline))
        serialized_cards = serialize_id(cards_cursor)

        for card in serialized_cards:
            card['content'] = strip_markdown(card.get('content', ''))

        return render_template("index.html", cards=serialized_cards, keyword=keyword)
        
    except Exception as e:
        print(f"Error: {e}")
        return "서버 오류가 발생했습니다.", 500