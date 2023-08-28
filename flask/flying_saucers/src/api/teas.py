from flask import Blueprint, jsonify, abort, request
from ..models import Tea, db

bp = Blueprint('teas', __name__, url_prefix='/teas')

# Show all


@bp.route('', methods=['GET'])
def index():
    teas = Tea.query.all()
    result = []
    for t in teas:
        result.append(t.serialize())
    return jsonify(result)

# Show by ID


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    t = Tea.query.get_or_404(id)
    return jsonify(t.serialize())

# Create by blend name


@bp.route('', methods=['POST'])
def create():
    if 'blend_name' not in request.json or 'caffeine' not in request.json:
        return abort(400)
    tea_in_database = Tea.query.filter_by(
        blend_name=request.json['blend_name']).first()
    if tea_in_database:
        return abort(409)
    t = Tea(
        blend_name=request.json['blend_name'],
        tasting_notes=request.json['tasting_notes'],
        date_of_purchase=request.json['date_of_purchase'],
        price=request.json['price'],
        origin=request.json['origin'],
        caffeine=request.json['caffeine'],
        supplier_id=request.json['supplier_id'],
        variety_type=request.json['variety_type'],
        brewing_temp_F=request.json['brewing_temp_F'],        
        brewing_temp_C=request.json['brewing_temp_C'],
        tsp_per_cup=request.json['tsp_per_cup']
    )
    db.session.add(t)
    db.session.commit()
    return jsonify(t.serialize())

# Delete by ID


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    t = Tea.query.get_or_404(id)
    try:
        db.session.delete(t)  # prepare to delete the tea from the database
        db.session.commit()  # delete the tea from the database
        return jsonify(True)
    except:
        return jsonify(False)  # if the tea is not deleted, return False

# Update by id


@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    t = Tea.query.get_or_404(id)
    if 'tea_blend' not in request.json and 'caffeine' not in request.json:
        return abort(400)
    try:
        for key, value in request.json.items():
            if hasattr(t, key):
                setattr(t, key, value)
        db.session.commit()
        return jsonify(t.serialize())
    except:
        return jsonify(False)

# Update by blend name


@bp.route('/<string:blend_name>', methods=['PATCH', 'PUT'])
def update(blend_name: str):
    t = Tea.query.get_or_404(blend_name)
    if 'tea_blend' not in request.json and 'caffeine' not in request.json:
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
    blend_name = request.args.get('blend_name')
    if not blend_name:
        return abort(400)
    teas = Tea.query.filter(Tea.blend_name.like(f'%{blend_name}%')).all()
    if not teas:
        return jsonify([])
    result = [teas.serialize() for tea in teas]
    return jsonify(result)


# Search by attribute
@bp.route('/searchbyattribute', methods=['GET'])
def searchbyattribute():
    key = request.args.get('key')
    value = request.args.get('value')
    if not key:
        return abort(400)
    try:
        teas = Tea.query.filter_by(**{key: value}).all()
        if teas:
            result = []
            for t in teas:
                tea_data = t.serialize()
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
        teas = Tea.query.filter_by(caffeine=(caffeine.lower() == 'true')).all()
        result = [tea.serialize() for tea in teas]
        if teas:
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
            teas = Tea.query.filter_by(caffeine=True).all()
        else:
            teas = Tea.query.filter_by(caffeine=False).all()

        result = [tea.serialize() for tea in teas]
        if teas:
            return jsonify(result)
        else:
            return jsonify([])
    except:
        return jsonify(False)
