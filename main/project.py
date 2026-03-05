from flask import render_template, Blueprint, request, jsonify
from datetime import datetime
from utils import serialize_id
from db import db

bp = Blueprint('project', __name__)



@bp.route('/api/projects/cards', methods=['GET'])
def project_list():
    # url에서 쿼리 스트링을 찾아야 함.
    # page라는 단어 추출
    # page 뒤에 있는 값을 기본값 1로 시작해서 추적
    page = int(request.args.get('page'), 1)
    # 한 페이지에 보이게 할 갯수
    limit = 4
    # 현재 페이지에서 보여줘야 할 데이터.
    # 4단위로 업데이트 되니, 2페이지에선 5번째 데이터부터 보여줘야 함
    skip = (page - 1) * limit

    cards = list(db.project_card.find().skip(skip).limit(limit))
    total = db.project_card.count_documents({})

    return jsonify({
        'result': 'success',
        'data': cards,
        'total': total,
        'page': page
    })

@bp.route('/api/projects/cards', methods=['POST'])
def project_post():
    return None

@bp.route('/api/projects/cards/<project_id>', methods=['GET'])
def detail(project_id):
    return None

@bp.route('/api/projects/cards/<project_id>', methods=['PATCH'])
def modify(project_id):
    return None

@bp.route('/api/projects/cards/<project_id>', methods=['DELETE'])
def delete(project_id):
    return None