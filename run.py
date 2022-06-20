from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False
# print(app.config)

db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method =='GET':
        user_data = User.query.all()
        result = [user.__dict__ for user in user_data]


if __name__ == '__main__':
    app.run(port=5010, debug=True)
