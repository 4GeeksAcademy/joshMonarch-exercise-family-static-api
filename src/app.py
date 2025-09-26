"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    try:
        members = jackson_family.get_all_members()
        if members:
            response_body = {"hello": "world",
                            "family": members}
            return jsonify(response_body), 200
        else:
            return {"error": "Members not found"}, 400
    except Exception as e:
        raise APIException(str(e), status_code=500)

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    try:
        member = jackson_family.get_member(id)
        if member:
            response_body = member
            return jsonify(response_body), 200
        else:
            return {"error", "Member not found"}, 400

    except Exception as e:
        raise APIException(str(e), status_code=500)

@app.route('/members', methods=['POST'])
def post_member():
    try:
        new_member = request.get_json()
        if new_member:
            members = jackson_family.add_member(new_member)
            response_body = {"hello": "world",
                            "family": members}
            return jsonify(response_body), 201
        else:
            return jsonify({"error": "Bad request"}), 400

    except Exception as e:
            raise APIException(str(e), status_code=500)

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        deleted = jackson_family.delete_member(id)
        if deleted:
            return jsonify({"done": True}), 200
        else:
            return jsonify({"error": "Member not found"}), 400

    except Exception as e:
        raise APIException(str(e), status_code=500)
    
# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
