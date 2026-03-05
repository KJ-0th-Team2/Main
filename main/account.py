from flask import render_template, Blueprint

bp = Blueprint('account', __name__)

@bp.route('/login')
def loginpage():
    return render_template('loginpage.html')

@bp.route("/login/access")
def login():
    return "로그인 되었습니다"