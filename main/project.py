from flask_jwt_extended import *
from flask import render_template, Blueprint, request, jsonify
from datetime import datetime
from utils import serialize_id
from db import db
from bson import ObjectId

bp = Blueprint('project', __name__)



@bp.route('/api/projects/cards', methods=['GET'])
def project_list():
    cards = list(db.project_card.find())
    
    return render_template(
        'index.html',
        project_cards=serialize_id(cards)
    )

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