from flask import Flask
from pymongo import MongoClient
from main import common, account

app = Flask(__name__)

app.register_blueprint(common.bp)
app.register_blueprint(account.bp)

if __name__ == '__main__':
    app.run(debug=True)