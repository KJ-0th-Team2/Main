from flask import Flask
from pymongo import MongoClient
from main import common, account
from flask_jwt_extended import *

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.jungle_wiki

app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = "123"
)

jwt = JWTManager(app)

app.register_blueprint(common.bp)
app.register_blueprint(account.bp)

user = list(db.user.find({}))

if not user:
    # TODO 이 경우에 유저 하나 생성하기
    
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