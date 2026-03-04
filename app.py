from flask import Flask
from main import indexTest
from pymongo import MongoClient

app = Flask(__name__)

app.register_blueprint(indexTest.bp)


# 이창원 TODO LIST
# LOCAL DB 연결

@app.route('/login')
def login():
    return
# 로그인 기능

if __name__ == '__main__':
    app.run(debug=True)