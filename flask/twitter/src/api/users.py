from flask import Blueprint, jsonify, abort, request
from ..models import User, db, Tweet, likes_table
import hashlib
import secrets

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('', methods = ['GET']) 
def index(): 
    users = User.query.all() 
    result = [] 
    for u in users: 
        result.append(u.serialize()) 
    return jsonify(result)
    
@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    u = User.query.get_or_404(id)
    return jsonify(u.serialize())  
    
@bp.route('', methods = ['POST']) 
def create(): 
    if 'username' not in request.json or 'password' not in request.json: 
        return abort(400) 
    if len(request.json['username']) <= 3 or len(request.json['password']) <= 8: 
        return abort(400)
    u = User( 
        username=request.json['username'],
        password=scramble(request.json['password']) 
    )
    db.session.add(u) 
    db.session.commit() 
    return jsonify(u.serialize()) 

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int): 
    u = User.query.get_or_404(id) 
    try: 
        db.session.delete(u) 
        db.session.commit() 
        return jsonify(True) 
    except: 
        return jsonify(False) 
        
