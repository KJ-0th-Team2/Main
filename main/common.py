from flask import render_template, Blueprint

bp = Blueprint('common', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/loginpage.html')
def loginpage():
    return render_template('loginpage.html')