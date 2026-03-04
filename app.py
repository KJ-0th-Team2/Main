from flask import Flask
from main import common, account
from pymongo import MongoClient

app = Flask(__name__)

app.register_blueprint(common.bp)
app.register_blueprint(account.bp)

if __name__ == '__main__':
    app.run(debug=True)