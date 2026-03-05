from flask import Flask, render_template
from db import db
from main import common, account, path
from flask_jwt_extended import *

app = Flask(__name__)


app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = "123"
)

jwt = JWTManager(app)

app.register_blueprint(common.bp)
app.register_blueprint(account.bp)
app.register_blueprint(path.bp)

user = list(db.user.find({}))

if not user:
    # 반환값 없으면 유저 하나 만들기
    user_data = {
        '_id' : 1,
        'username' : 'test',
        'password' : '123'
    }
        
    db.user.insert_one(user_data)

    data = db.user.find_one({})
    print(data)
else:
    print("이미 있음")


if __name__ == '__main__':
    app.run(debug=True)