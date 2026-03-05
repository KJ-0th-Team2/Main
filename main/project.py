from flask import render_template, Blueprint, request, jsonify
from datetime import datetime
from utils import serialize_id
from db import db
from bson import ObjectId

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
    title_receieve = request.json['title_text']
    content_receive = request.json['content_text']
    team_receive = request.json['team_number']
    member_receive = request.json['member_list']

    if title_receieve is None or content_receive is None or member_receive is None:
        return jsonify({
            'result': 'fail',
            'msg': '입력하지 않은 요소가 있습니다.'
        }), 400
    if len(member_receive) < 3:
        return jsonify({
            'result': 'fail',
            'msg': '멤버 이름을 정확히 입력해주세요.'
        }), 400

    post_data = {
        'title': title_receieve,
        'content': content_receive,
        'team': team_receive,
        'member': member_receive
    }

    db.project_card.insert_one(post_data)

    return jsonify({
        'result': 'success',
        'msg': '업로드 되었습니다.'
    }), 200

@bp.route('/api/projects/cards/<project_id>', methods=['GET'])
def detail(project_id):
    project_id = ObjectId(project_id)

    value = db.project_card.find_one({'_id': project_id})
    value['_id'] = str(value['_id'])

    return jsonify({
        'result': 'success',
        'msg': '데이터 호출',
        'data': value
    })

@bp.route('/api/projects/cards/<project_id>', methods=['PATCH'])
def modify(project_id):
    title_receieve = request.json['title_text']
    content_receive = request.json['content_text']
    team_receive = request.json['team_number']
    member_receive = request.json['member_list']

    if title_receieve is None or content_receive is None or member_receive is None:
        return jsonify({
            'result': 'fail',
            'msg': '입력하지 않은 요소가 있습니다.'
        }), 400
    if len(member_receive) < 3:
        return jsonify({
            'result': 'fail',
            'msg': '멤버 이름을 정확히 입력해주세요.'
        }), 400

    post_data = {
        'title': title_receieve,
        'content': content_receive,
        'team': team_receive,
        'member': member_receive
    }

    db.project_card.update_one({'_id':project_id}, {'$set': post_data})
    return jsonify({
        'result': 'success',
        'msg': '수정 성공!'
    })

@bp.route('/api/projects/cards/<project_id>', methods=['DELETE'])
def delete(project_id):
    return None