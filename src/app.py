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
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()

    
    return jsonify(members), 200


@app.route('/members', methods=['POST'])
def add_new_member():
    # This is how you can use the Family datastructure by calling its methods
    member = request.get_json()

    if not member:
        return ({"message": "body is required"}),400

    first_name = member.get("first_name")
    age = member.get("age")
    lucky_numbers = member.get("lucky_numbers")

    first_name_is_string = isinstance(first_name,str)
    age_is_number = isinstance(age, int)
    lucky_numbers_is_list = isinstance(lucky_numbers, list)

    if not first_name_is_string or not age_is_number or not lucky_numbers_is_list:
        return jsonify({"message":"Not fulfilled required fields"})

    new_member = jackson_family.add_member(member)

    return jsonify(new_member), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    # This is how you can use the Family datastructure by calling its methods
    jackson_family.delete_member(id)
    return jsonify({"done":True}), 200

@app.route('/members/<int:id>', methods=['GET'])
def single_member(id):
    member = jackson_family.get_member(id)
    if not member:
        return ({"message":"not member"})
    return jsonify(member), 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
