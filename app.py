# from flask import Flask, jsonify
# from pymongo import MongoClient

# app = Flask(__name__)

# # Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client["your_database"]
# collection = db["your_collection"]

# @app.route("/get_data")
# def get_data():
#     data = list(collection.find({}, {"_id": 0}))
#     return jsonify(data)

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5001, debug=True)
from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests

# Set up MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database"]
collection = db["your_collection"]

@app.route('/api/data', methods=['GET'])
def get_data():
    data = list(collection.find({}, {"_id": 0}))  # Exclude _id field
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)