from pymongo import MongoClient

# client = MongoClient('mongodb://test:test@43.201.78.121', 27017)
client = MongoClient('localhost', 27017)
db = client.jungle_wiki