import datetime
import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)


@app.route('/users/', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        user_data = User.query.all()
        result = [user.to_dict() for user in user_data]
        return jsonify(result)
    if request.method == 'POST':
        new_user = json.loads(request.data)
        new_user_obj = User(
            id=new_user['id'],
            first_name=new_user['first_name'],
            last_name=new_user['last_name'],
            age=new_user['age'],
            email=new_user['email'],
            role=new_user['role'],
            phone=new_user['phone'],
        )
        db.session.add(new_user_obj)
        db.session.commit()
        return "Пользователь добавлен", 200


@app.route('/orders/', methods=['GET', 'POST'])
def get_orders():
    if request.method == 'GET':
        order_data = Order.query.all()
        result = [order.to_dict() for order in order_data]
        return jsonify(result)
    if request.method == 'POST':
        new_order = json.loads(request.data)
        month_start, day_start, year_start = [int(_) for _ in new_order['start_date'].split('/')]
        month_end, day_end, year_end = [int(_) for _ in new_order['end_date'].split('/')]
        new_order_obj = Order(
            id=new_order['id'],
            name=new_order['name'],
            description=new_order['description'],
            start_date=datetime.date(year=year_start, month=month_start, day=day_start),
            end_date=datetime.date(year=year_end, month=month_end, day=day_end),
            address=new_order['address'],
            price=new_order['price'],
            customer_id=new_order['customer_id'],
            executor_id=new_order['executor_id'],
        )
        db.session.add(new_order_obj)
        db.session.commit()
        return "Заказ добавлен", 200


@app.route('/offers/', methods=['GET', 'POST'])
def get_offers():
    if request.method == 'GET':
        offer_data = Offer.query.all()
        result = [offer.to_dict() for offer in offer_data]
        return jsonify(result)
    if request.method == 'POST':
        new_offer = json.loads(request.data)
        new_offer_obj = Offer(
            id=new_offer['id'],
            order_id=new_offer['order_id'],
            executor_id=new_offer['executor_id'],
        )
        db.session.add(new_offer_obj)
        db.session.commit()
        return "Предложение добавлено", 200


@app.route('/users/<int:user_id>/', methods=['GET', 'PUT', 'DELETE'])
def one_user(user_id):
    user = db.session.query(User).get(user_id)
    if user is None:
        return "Пользователь не найден", 404
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age']
        user.email = user_data['email']
        user.role = user_data['role']
        user.phone = user_data['phone']
        db.session.add(user)
        db.session.commit()
        return f"Пользователь с ID={user_id} изменен", 200
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return f"Пользователь с ID={user_id} удален", 200


@app.route('/orders/<int:order_id>/', methods=['GET', 'PUT', 'DELETE'])
def one_order(order_id):
    order = db.session.query(Order).get(order_id)
    if order is None:
        return "Заказ не найден"
    if request.method == 'GET':
        return jsonify(order.to_dict())
    elif request.method == 'PUT':
        order_data = json.loads(request.data)
        month_start, day_start, year_start = [int(_) for _ in order_data['start_date'].split('/')]
        month_end, day_end, year_end = [int(_) for _ in order_data['end_date'].split('/')]
        order.name = order_data['name']
        order.description = order_data['description']
        order.start_date = datetime.date(year=year_start, month=month_start, day=day_start)
        order.end_date = datetime.date(year=year_end, month=month_end, day=day_end)
        order.address = order_data['address']
        order.price = order_data['price']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']
        db.session.add(order)
        db.session.commit()
        return f"Заказ с ID={order_id} изменен", 200
    elif request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return f"Заказ с ID={order_id} удален", 200


@app.route('/offers/<int:offer_id>/', methods=['GET', 'PUT', 'DELETE'])
def one_offer(offer_id):
    offer = db.session.query(Offer).get(offer_id)
    if offer is None:
        return "Предложение не найдено", 404
    if request.method == 'GET':
        return jsonify(offer.to_dict())
    elif request.method == 'PUT':
        offer_data = json.loads(request.data)
        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']
        db.session.add(offer)
        db.session.commit()
        return f"Предложение с ID={offer_id} изменено", 200
    elif request.method == 'DELETE':
        db.session.delete(offer)
        db.session.commit()
        return f"Предложение с ID={offer_id} удалено", 200


if __name__ == '__main__':
    app.run(port=5010, debug=True)
