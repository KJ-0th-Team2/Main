from flask_jwt_extended import *
from datetime import timedelta # refresh 토큰 시간제한
from flask import render_template, Blueprint, request, jsonify, make_response
from db import db # 순환 호출 에러 해결용
import re # 정규 표현식 용도
import bcrypt

bp = Blueprint('account', __name__)

# 회원가입
@bp.route("/api/users/post", methods=['POST'])
def register():
    member_id = request.json['input_num']
    id_receive = request.json['input_id']
    pw_receive = request.json['input_pwd']

    if member_id is None or id_receive is None or pw_receive is None:
        return jsonify({
            'result': 'fail',
            'msg': '모든 칸을 입력해주세요.'
        }), 400
    
    if not re.match(r'^[a-z0-9]+$', id_receive):
        return jsonify({
            'result': 'fail',
            'msg': '아이디는 소문자와 숫자만 가능합니다.'
        }), 400
    
    if (db.user.find_one({'username':id_receive})):
        return jsonify({
            'result': 'fail',
            'msg': '중복된 아이디입니다.'
        }), 409
    
    hashed_password = bcrypt.hashpw(pw_receive.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    user_data = {
        '_id': member_id,
        'username': id_receive,
        'password': hashed_password
    }

    db.user.insert_one(user_data)

    return jsonify({
        'result': 'success',
        'msg': '회원가입 완료',
    }), 200

@bp.route("/api/auth/check_id", methods=['GET'])
def check_id():
    id_receive = request.args.get('query')

    if (db.user.find_one({'username':id_receive})):
        return jsonify({
            'result': 'fail',
            'msg': '중복된 아이디입니다.'
        }), 409

    return jsonify({
        'result': 'success',
        'msg': '사용 가능한 아이디입니다.'
    }), 200

# 아이디 중복확인
@bp.route("/api/auth/tokentest", methods=['GET'])
# 밑에 jwt_required로 토큰 검사
@jwt_required()
def token_test():

    return jsonify({
        'success': 'success',
        'msg': 'jwt_required()로 검증. 현재 access_token 토큰 존재'
    }), 200


@bp.route("/api/auth/refresh", methods=['POST'])
# jwt_required로 refresh 토큰 검사
@jwt_required(refresh=True)
def refresh_token():
    identity_value = get_jwt_identity()
    new_access_token = create_access_token(identity = identity_value)

    return jsonify({ 
        'result': 'success',
        'userinfo': identity_value,
        'access_token': new_access_token
    }), 200

# @jwt_required는 헤더로 수신한 Access 토큰의 유효성을 검증하는 데코레이터
# 즉 프론트엔드에서 Access_token값을 헤더로 보내야 함. Authorization
@bp.route("/api/auth/login", methods=['POST'])
def login():
    # TODO JWT 인증키는 app.py에서 정의
    id_receive = request.json['input_id']
    pw_receive = request.json['input_pwd']

    # 아이디 검증
    # 입력받은 아이디가 실제로 존재하는 값인지 조회
    value = db.user.find_one({"username":f"{id_receive}"})

    if id_receive is None or pw_receive is None:
        return jsonify({
            'result': 'fail',
            'msg': '아이디 또는 비밀번호를 입력해주세요.'
        }), 403
    if value is None:
        return jsonify({
            'result': 'fail',
            'msg': '아이디 혹은 비밀번호를 잘못 입력했습니다.'
        }), 403
    
    # hashed = bcrypt.hashpw(pw_receive.encode('UTF-8'), bcrypt.gensalt()).decode('utf-8')
    user_data = db.user.find_one({'username':id_receive})

    db_pass = user_data['password']

    # 비밀번호 인증
    if not bcrypt.checkpw(pw_receive.encode('UTF-8'), db_pass.encode('UTF-8')):
        return jsonify ({
            'result': 'fail',
            'msg': '아이디 혹은 비밀번호를 잘못 입력했습니다.'
        }), 403
    
    access_token = create_access_token(identity=id_receive)
    refresh_token = create_refresh_token(identity=id_receive, expires_delta=timedelta(minutes=10))

    response = make_response(jsonify({
        'result': 'success',
        'msg': f'정상 작동',
        'access_token': access_token
    }), 200)
    response.set_cookie("refresh_token_cookie", refresh_token, httponly=True)

    return response

@bp.route("/api/auth/logout", methods=['DELETE'])
@jwt_required(refresh=True)
def logout():
    response = make_response(jsonify({
        'result': 'success',
        'msg': '로그아웃 되었습니다.'
    }), 200)

    unset_refresh_cookies(response)
    return response

@bp.route("/api/user/me", methods=['GET'])
@jwt_required()
def login_check():
    return jsonify({"logedin": True})