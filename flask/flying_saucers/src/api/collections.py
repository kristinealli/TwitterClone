from flask import Blueprint, jsonify, abort, request
from ..models import Collection, Tea, db
import datetime

bp = Blueprint('Collections', __name__, url_prefix='/Collections')

# Show all


@bp.route('', methods=['GET'])
def index():
    Collections = Collection.query.all()
    result = []
    for c in Collections:
        result.append(c.serialize())
    return jsonify(result)

# Show by ID


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    c = Collection.query.get_or_404(id)
    return jsonify(c.serialize())

# Create by collection name


@bp.route('', methods=['POST'])
def create():
    if 'user_id' not in request.json and 'collection_name' not in request.json: #Will confirm user is logged in to create a collection
        return abort(400)
    Collection_in_database = Collection.query.filter_by(
        collection_name=request.json['collection_name']).first()
    if Collection_in_database:
        return abort(409)
    c = Collection(
        date_created = datetime.now(),
        user_id=request.json['user_id'],
        collection_name=request.json['collection_name']
    )
    if 'teas' in request.json and isinstance(request.json['teas'], list):
        for tea_id in request.json['teas']:
            tea = Tea.query.get(tea_id)
            if tea:
                c.teas.append(tea)
    db.session.add(c)
    db.session.commit()
    return jsonify(c.serialize())

# Delete by ID


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    c = Collection.query.get_or_404(id)
    try:
        db.session.delete(c)  # prepare to delete the Collection from the database
        db.session.commit()  # delete the Collection from the database
        return jsonify(True)
    except:
        return jsonify(False)  # if the Collection is not deleted, return False

# Update collection name

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    c = Collection.query.get_or_404(id)
    if 'collection_name' not in request.json and 'teas' not in request.json:
        return abort(400)
    try:
        for key, value in request.json.items():
            if hasattr(c, key):
                setattr(c, key, value)
        db.session.commit()
        return jsonify(c.serialize())
    except:
        return jsonify(False)

# Update by blend name


@bp.route('/<string:blend_name>', methods=['PATCH', 'PUT'])
def update(blend_name: str):
    t = Collection.query.get_or_404(blend_name)
    if 'Collection_blend' not in request.json and 'caffeine' not in request.json:
        return abort(400)
    try:
        for key, value in request.json.items():
            if hasattr(t, key):
                setattr(t, key, value)
        db.session.commit()
        return jsonify(t.serialize())
    except:
        return jsonify(False)

# Search


@bp.route('/search', methods=['GET'])
def search():
    blend_name = request.args.get('collection_name')
    if not blend_name:
        return abort(400)
    Collections = Collection.query.filter(Collection.blend_name.like(f'%{blend_name}%')).all()
    if not Collections:
        return jsonify([])
    result = [Collections.serialize() for Collection in Collections]
    return jsonify(result)


# Search by attribute
@bp.route('/searchbyattribute', methods=['GET'])
def searchbyattribute():
    key = request.args.get('key')
    value = request.args.get('value')
    if not key:
        return abort(400)
    try:
        Collections = Collection.query.filter_by(**{key: value}).all()
        if Collections:
            result = []
            for t in Collections:
                Collection_data = t.serialize()
            return jsonify(result)
        else:
            return jsonify([])
    except:
        return jsonify(False)


# Search by caffeine
@bp.route('/caffeine', methods=['GET'])
def findcaffeine():
    caffeine = request.args.get('caffeine')
    if not caffeine:
        return abort(400)
    try:
        Collections = Collection.query.filter_by(caffeine=(caffeine.lower() == 'true')).all()
        result = [Collection.serialize() for Collection in Collections]
        if Collections:
            return jsonify(result)
        else:
            return jsonify([])
    except:
        return jsonify(False)


@bp.route('/nocaffeine', methods=['GET'])
def findnocaffeine():
    caffeine = request.args.get('caffeine')
    if not caffeine:
        return abort(400)
    try:
        if caffeine.lower() == 'true':
            Collections = Collection.query.filter_by(caffeine=True).all()
        else:
            Collections = Collection.query.filter_by(caffeine=False).all()

        result = [Collection.serialize() for Collection in Collections]
        if Collections:
            return jsonify(result)
        else:
            return jsonify([])
    except:
        return jsonify(False)
