from flask import render_template, Blueprint

bp = Blueprint('common', __name__)

# 어카운트

@bp.route('/')
def index():
    return render_template('index.html')