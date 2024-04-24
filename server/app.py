#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakery_list = []
    for bakery in bakeries:
        bakery_dict = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'baked_goods': [{'id':bg.id, 'name':bg.name, 'price':bg.price} for bg in bakery.baked_goods],
        }
        bakery_list.append(bakery_dict)
    return make_response(jsonify(bakery_list), 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict = {
        'id': bakery.id,
        'name': bakery.name,
        'created_at': bakery.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'baked_goods': [{'id': bg.id, 'name': bg.name, 'price': bg.price} for bg in bakery.baked_goods],
    }
    return make_response(jsonify(bakery_dict), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_good_list = []
    for bg in baked_goods:
        baked_good_dict = {
            'id': bg.id,
            'name': bg.name,
            'price': bg.price,
            'created_at': bg.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        baked_good_list.append(baked_good_dict)
    return make_response(jsonify(baked_good_list), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good:
        baked_good_dict = {
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price,
            'created_at': baked_good.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        return make_response(jsonify(baked_good_dict), 200)
    else:
        return make_response(jsonify(error='No baked goods found'), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)