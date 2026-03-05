from flask_jwt_extended import *
from datetime import timedelta
from flask import render_template, Blueprint, request, jsonify, make_response
from db import db

bp = Blueprint('account', __name__)

@bp.route('/login')
def loginpage():
    return render_template('loginpage.html')

# 회원가입 기능 임시 비활성화

# @bp.route("/user/post", methods=['POST'])
# def register():
#     id_receive = request.json['input_id']
#     pw_receive = request.json['input_pwd']


#     return



@bp.route("/auth/tokentest", methods=['GET'])
# 밑에 jwt_required로 토큰 검사
@jwt_required()
def token_test():

    return jsonify({
        'success': 'success',
        'msg': 'jwt_required()로 검증. 현재 access_token 토큰 존재'
    }), 200


@bp.route("/auth/refresh", methods=['POST'])
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
@bp.route("/auth/login", methods=['POST'])
def login():
    # TODO JWT 인증키는 app.py에서 정의
    id_receive = request.json['input_id']
    pw_receive = request.json['input_pwd']

    # 아이디 검증
    # 입력받은 아이디가 실제로 존재하는 값인지 조회
    value = db.user.find_one({"username":f"{id_receive}"})

    if value is None:
        return jsonify({
            'result': 'fail',
            'msg': 'ID가 없습니다'
        }), 403
    
    if (pw_receive != value['password']):
        return jsonify ({
            'result': 'fail',
            'msg': 'pw 불일치'
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
