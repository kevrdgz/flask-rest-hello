"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, People, Planets
#from models import Person

#jwt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this "super secret" with something else!
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
# get user
@app.route('/user', methods=['GET'])
def list_user():
    all_user = User.query.all()
    all_user = list(map(lambda x: x.serialize(), all_user))
    return jsonify(all_user), 200
# get planets
@app.route('/planets', methods=['GET'])
def list_planets():
    all_planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))
    return jsonify(all_planets), 200
# get people 
@app.route('/people', methods=['GET'])
def list_people():
    all_people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))
    return jsonify(all_people), 200

# get todos los favoritos 
@app.route('/allfavorites', methods=['GET'])
def list_allfavorites():
    all_favorites = Favorites.query.all()
    all_favorites = list(map(lambda x: x.serialize(), all_favorites))
    return jsonify(all_favorites), 200


#get favorites de  un usuario
@app.route("/favorites", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    getfavs  = Favorites.query.filter_by(user_id = current_user_id)
    getfavs = list(map(lambda x: x.serialize(), getfavs))
    
    return jsonify(getfavs), 200


# post user
@app.route('/user', methods=['POST'])
def create_user():
    body = request.get_json() # get the request body content
    if body is None:
         return "The request body is null", 400
    if 'password' not in body:
        return 'You need to specify the password',400
    if 'email' not in body:
        return 'You need to specify the email', 400
    if 'username' not in body:
        return 'You need to specify the username', 400
 
   
        
    user = User()
        
    user.email = body['email']
    user.password = body['password']
    user.username = body['username']
    user.is_active =True
    #agrega user a la base de datos
    db.session.add(user)
    #guarda los cambios
    db.session.commit()

    response_body = {
        "msg": "PURA VIDA!"
        }

    return jsonify(response_body), 200

# post favorites crea favorito
@app.route('/favorites', methods=['POST'])
@jwt_required()
def create_favorite():
    current_user_id = get_jwt_identity()
    
   
    body = request.get_json() # get the request body content
    if body is None:
         return "The request body is null", 400
    if 'name' not in body:
        return 'You need to specify the favorite name',400
  
 
        
    favorites = Favorites()
    favorites.user_id = current_user_id
    favorites.name = body['name']
  
    #agrega user a la base de datos
    db.session.add(favorites)
    #guarda los cambios
    db.session.commit()

    getfavs  = Favorites.query.filter_by(user_id = current_user_id)
    getfavs = list(map(lambda x: x.serialize(), getfavs))
    
    return jsonify(getfavs), 200
#delete favorites 
@app.route('/favorites', methods=['DELETE'])
@jwt_required()
def delete_favorite():
    current_user_id = get_jwt_identity()
    
   
    body = request.get_json() # get the request body content
    if body is None:
         return "The request body is null", 400
    if 'id' not in body:
        return 'You need to specify the favorite id',400
  
    getfavs  = Favorites.query.filter_by(user_id = current_user_id , id = body['id']).first()
    
        
    
  
    #agrega user a la base de datos
    db.session.delete(getfavs)
    #guarda los cambios
    db.session.commit()

    getfavs  = Favorites.query.filter_by(user_id = current_user_id)
    getfavs = list(map(lambda x: x.serialize(), getfavs))
    

    
    
    return jsonify(getfavs), 200

#crear  token
@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    user = User.query.filter_by(username=username, password=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    getfavs  = Favorites.query.filter_by(user_id = user.id)
    getfavs = list(map(lambda x: x.serialize(), getfavs))
    return jsonify({ "token": access_token, "user_id": user.id , "list_fav" : getfavs})

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
