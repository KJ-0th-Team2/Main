from flask_jwt_extended import *
from flask import render_template, Blueprint, request, jsonify, make_response
from db import db

bp = Blueprint('account', __name__)

@bp.route('/login')
def loginpage():
    return render_template('loginpage.html')

@bp.route("/auth")
def auth():

    return

# 회원가입 기능 임시 비활성화

# @bp.route("/user/post", methods=['POST'])
# def register():
#     id_receive = request.json['input_id']
#     pw_receive = request.json['input_pwd']


#     return

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
        })
    
    if (pw_receive != value['password']):
        return jsonify ({
            'result': 'fail',
            'msg': 'pw 불일치'
        })
    
    access_token = create_access_token(identity=id_receive, expires_delta=None)
    refresh_token = create_refresh_token(identity=id_receive, expires_delta=None)

    response = make_response(jsonify({
        'result': 'success',
        'msg': f'정상 작동',
    }))

    response.set_cookie


    return jsonify({
        'result': 'success',
        'msg': f'정상 전달 {value}',
        'access_token': access_token,
        'refresh_token': refresh_token
    })