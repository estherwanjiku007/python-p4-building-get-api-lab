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
    all_bakeries_list=[]
    all_bakeries=Bakery.query.all()
    for bakery in all_bakeries:
        bakery_dict={
            "id":bakery.id,
            "name":bakery.name,
            "created_at":bakery.created_at,
            "updated_at":bakery.updated_at
        }
        all_bakeries_list.append(bakery_dict)        
    response=make_response(all_bakeries_list,200)
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    baked_goods_list=[]
    bakery=Bakery.query.filter(Bakery.id==id).first()
    baked_goods=BakedGood.query.filter(BakedGood.bakery_id==id)
    for baked_good in baked_goods:
        baked_goods_list.append(baked_good)
    bakery_dict={
        "id":bakery.id,
        "name":bakery.name,
        "created_at":bakery.created_at,
        "updated_at":bakery.updated_at,
        "baked_goods":baked_goods_list
    }
    response=make_response(bakery_dict,200)
    return response
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods=BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list=[]
    for baked_good in baked_goods:
        baked_good_dict={
            "id":baked_good.id,
            "name":baked_good.name,
            "price":baked_good.price,
            "bakery_id":baked_good.bakery_id,
            "created_at":baked_good.created_at,
            "updated_at":baked_good.updated_at,
        }
        baked_goods_list.append(baked_good_dict)        
    response=make_response(baked_goods_list,200)
    return response
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good=BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    baked_good_dict={
        "id":baked_good.id,
            "name":baked_good.name,
            "price":baked_good.price,
            "bakery_id":baked_good.bakery_id,
            "created_at":baked_good.created_at,
            "updated_at":baked_good.updated_at,        
    }
    response=make_response(baked_good_dict,200)
    return response

# @app.route("/GET/bakeries")
# def get_all_bakeries():    
#     all_bakeries=Bakery.query.all()
#     for bakery in all_bakeries:
#         bakery_dict={
#             "id":bakery.id,
#             "name":bakery.name,
#             "created_at":bakery.created_at,
#             "updated_at":bakery.updated_at
#         }
        
#     response=make_response(bakery_dict,200)
#     return response
if __name__ == '__main__':
    app.run(port=5555, debug=True)
