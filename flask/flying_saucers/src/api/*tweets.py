from flask import Blueprint, jsonify, abort, request
from ..models import Tweet, User, db

bp = Blueprint('teas', __name__, url_prefix='/teas') 

@bp.route('', methods = ['GET']) 
# takes in a path and a list of HTTP verbs, empty path because it is already defined in blueprint
# decorator - function will be called when the path is /tweets and the HTTP verb is GET
def index(): 
    teas = teas.query.all() #ORM select query - get all tweets from the database
    result = [] #create an empty list named result
    for t in teas: #iterate through the tweets
        result.append(t.serialize()) #serialize each tweet and add it to the result list, dictionary
    return jsonify(result) #returnt the result list as JSON

@bp.route('/<int:id>', methods = ['GET'])
def show (id: int):
    t = Tweet.query.get_or_404(id) #ORM select query - get the tweet with the given id or return 404
    return jsonify(t.serialize()) #serialize the tweet and retrun it as JSON
    
@bp.route('', methods = ['POST']) #decorator - function to be called when the path is /tweets and the HTTP verb is POST
def create(): 
    if 'user_id' not in request.json or 'content' not in request.json: #check if request body contains user_id and content
        return abort(400) #if not, return Bad Request
    User.query.get_or_404(request.json['user_id']) #ORM select query - get the user with the given user_id or return 404
    t = Tweet( 
        user_id=request.json['user_id'], #creates a new tweet object with the given user_id and content
        content=request.json['content'] #creates a new tweet object with the given user_id and content
    )
    db.session.add(t) # prepare to insert the tweet into the database
    db.session.commit() #insert the tweet into the database
    return jsonify(t.serialize()) #serialize the tweet and return it as JSON
    
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int): 
    t = Tweet.query.get_or_404(id) #ORM select query - get the tweet with the given id or return 404
    try: 
        db.session.delete(t) #prepare to delete the tweet from the database
        db.session.commit() #delete the tweet from the database
        return jsonify(True) 
    except: 
        return jsonify(False) #if the tweet is not delete, return False
        
@bp.route('/<int:id>/liking_users', methods=['GET'])
def liking_users(id: int):
    t = Tweet.query.get_or_404(id)
    result = []
    for u in t.liking_users:
        result.append(u.serialize())
    return jsonify(result)
