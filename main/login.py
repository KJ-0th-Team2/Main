from flask import Blueprint

bp = Blueprint('login', __name__)

@bp.route("login")
def login():
    return "로그인 되었습니다"