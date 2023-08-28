from flask import Blueprint, jsonify, abort, request
from ..models import User, db, Tweet, likes_table
import hashlib
import secrets
import sqlalchemy


def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['GET'])
def index():
    users = User.query.all()
    result = []
    for u in users:
        result.append(u.serialize())
    return jsonify(result)


@bp.route('/<int:id>', methods=['GET'])#
def show(id: int): 
    u = User.query.get_or_404(id) #
    return jsonify(u.serialize())


@bp.route('', methods=['POST'])
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


@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    u = User.query.get_or_404(id)
    if 'username' not in request.json and 'password' not in request.json:
        return abort(400)
    if 'username' in request.json:
        if len(request.json['username']) < 3:
            return abort(400)
        u.username = request.json['username']
    if 'password' in request.json:
        if len(request.json['password']) < 8:
            return abort(400)
        u.password = scramble(request.json['password'])
    try:
        db.session.commit()
        return jsonify(u.serialize())
    except:
        return jsonify(False)


@bp.route('/<int:id>/liked_tweets', methods=['GET'])
def liked_tweets(id: int):
    u = User.query.get_or_404(id)
    result = []
    for t in u.liked_tweets:
        result.append(t.serialize())
    return jsonify(result)


@bp.route('/<int:id>/likes', methods=['POST'])
def like(id: int):
    if 'tweet_id' not in request.json:
        return abort(400)
    u = User.query.get_or_404(id)
    t = Tweet.query.get_or_404(request.json['tweet_id'])
    if u in t.liking_users:
        return jsonify(False)
    stmt = sqlalchemy.insert(likes_table).values(user_id=u.id, tweet_id=t.id)
    db.session.execute(stmt)
    db.session.commit()
    return jsonify(True)


@bp.route('/<int:user_id>/likes/<int:tweet_id>', methods=['DELETE'])
def unlike(user_id: int, tweet_id: int):
    u = User.query.get_or_404(user_id)
    t = Tweet.query.get_or_404(tweet_id)
    if u not in t.liking_users:
        return jsonify(False)
    stmt = sqlalchemy.delete(likes_table).where(
        likes_table.c.user_id == user_id).where(likes_table.c.tweet_id == tweet_id)
    db.session.execute(stmt)
    db.session.commit()
    return jsonify(True)
