from flask import render_template, Blueprint, request, jsonify
from pymongo import MongoClient

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

