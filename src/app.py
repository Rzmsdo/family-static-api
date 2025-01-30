"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

##### Realiza GET total####
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
  
    return jsonify(members), 200

##### Realiza Get individual####
@app.route('/member/<int:id>', methods =['GET'])
def get_single_member(id):
    
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
   
    return jsonify({"error": "Miembro en la familia no encontrado"}), 404
   
##### Realiza POST ####
@app.route('/member', methods =['POST'])
def add_miembro():
    member = request.json
    if not member:
        return jsonify({"error": "No se pudo añadir ningun mienbro"}), 400
    
    jackson_family.add_member(member)
    
    return jsonify({"mensaje": "Un nuevo miembro añadido a la familia"}), 200
    
  

##### Realiza DELETE ####  
@app.route('/member/<int:id>', methods =['DELETE'])
def delete_single_member(id):
   
    member =jackson_family.get_member(id)
    
    if member:
        jackson_family.delete_member(id)

        return jsonify({"mensaje": "Miembro eliminado correctamente"}), 200
    
    return jsonify({"error": "No se pudo eliminar el miembro"}), 400
   
   
        






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
