from flask import render_template, Blueprint,request

from db import db
from utils import serialize_id

#
bp = Blueprint('path', __name__)


@bp.route('/detail')
def detail():
    return render_template('detail.html')

@bp.route('/upload')
def upload():
    return render_template('upload.html')

@bp.route('/update')
def update():
    return render_template('update.html')

@bp.route('/history')
def history():
    return render_template('history.html')

@bp.route("/")
def index():
    # 1. 정렬 파라미터 가져오기
    sort_param = request.args.get("sort", "latest")
    
    # 2. 정렬 맵 구성 (latest는 -1, old는 1)
    SORT_MAP = {
        "latest": ("created_at", -1),
        "old": ("created_at", 1),      # 오래된순 추가
        "views": ("view_count", -1),
        "comments": ("comment_count", -1)
    }
    
    # 매칭되는 정렬 기준이 없으면 기본값인 'latest' 적용
    field, order = SORT_MAP.get(sort_param, SORT_MAP["latest"])

    try:
        # 3. DB 조회 및 정렬 적용
        # db 객체는 이미 jungle_wiki DB를 가리키므로 컬렉션 이름인 card를 사용합니다.
        cards_cursor = list(db.card.find({}).sort(field, order))
        
        # 4. ObjectId 문자열 변환
        serialized_cards = serialize_id(cards_cursor)
        
        # 5. 템플릿 렌더링
        return render_template("index.html", cards=serialized_cards)
        
    except Exception as e:
        print(f"Error: {e}")
        return "서버 오류가 발생했습니다.", 500