from flask import Flask, render_template
from datetime import timedelta, datetime, timezone
from db import db
from main import common, account, path, card, project
from flask_jwt_extended import *
import bcrypt

app = Flask(__name__)


app.config.update(
    DEBUG = True,
    JWT_TOKEN_LOCATION = ['headers','cookies'],
    JWT_COOKIE_CSRF_PROTECT = False,
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=5),
    JWT_SECRET_KEY = "123"
)

jwt = JWTManager(app)

app.register_blueprint(common.bp)
app.register_blueprint(account.bp)
app.register_blueprint(path.bp)
app.register_blueprint(card.bp)
app.register_blueprint(project.bp)

user = db.user.find_one({'username':'test'})

if not user:
    # 반환값 없으면 유저 하나 만들기
    passwd = '123'
    user_data = {
        '_id' : 1,
        'username' : 'test',
        'password' : bcrypt.hashpw(passwd.encode('UTF-8'), bcrypt.gensalt()).decode('utf-8')
    }
        
    db.user.insert_one(user_data)

    data = db.user.find_one({})
    print(data)
else:
    db.user.delete_one({'username':'test'})

    passwd = '123'
    user_data = {
        '_id' : 1,
        'username' : 'test',
        'password' : bcrypt.hashpw(passwd.encode('UTF-8'), bcrypt.gensalt()).decode('utf-8')
    }
        
    db.user.insert_one(user_data)

    data = db.user.find_one({})
    print(data)

    print("기존계정 지우고 해시 passwd 포함한 계정 생성")

post = list(db.card.find({}))

if not post:
    post_data = {
        'title': '제목입니다.',
        'content': '내용내용내용내용',
        'version': 1,
        'created_at': datetime.now(timezone.utc)
    }

    db.card.insert_one(post_data)

    data = db.card.find_one({})

    print(data)
else:
    print("카드 이미 있음")


prcard = list(db.project_card.find({}))

if prcard is None:
    card_data = {
        'title' : '정글 위키와 함께하는 3박 4일간의 여정',
        'content' : 'Jinja와 같은 새로운 기능, JWT를 이용한 보안 등, 다양한 도전을 시도해본 프로젝트',
        'team' : 2,
        'member' : ['이우진', '임재환', '임가인', '이창원']
    }
    db.project_card.insert_one(card_data)
else:
    print("있으면 스킵")
    


# 서버용 코드

# if __name__ == '__main__':
#     app.run('0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    app.run(debug=True)