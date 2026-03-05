from flask import render_template, Blueprint

#
bp = Blueprint('path', __name__)


@bp.route('/detail')
def detail():
    return render_template('detail.html')

@bp.route('/upload')
def upload():
    return render_template('upload.html')

@bp.route('/update')
def update():
    return render_template('update.html')

@bp.route('/history')
def history():
    return render_template('history.html')

@bp.route('/')
def index():
    return render_template('index.html')