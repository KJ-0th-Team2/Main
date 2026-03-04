from flask import render_template, Blueprint, request

bp = Blueprint('account', __name__)

@bp.route('/login')
def loginpage():
    return render_template('loginpage.html')

@bp.route("/auth")
def auth():

    return

# 임시로 회원가입
@bp.route("/user/post", methods=['POST'])
def register():
    id_receive = request.json['input_id']
    pw_receive = request.json['input_pwd']


    return