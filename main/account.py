from flask import render_template, Blueprint, request

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

@bp.route("/auth/login")
def login():
    # TODO JWT 인증키는 app.py에서 정의
    return