
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, request, Response, redirect
from routes import route_path

app = Flask(__name__)
app.register_blueprint(route_path)
#add database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///addressData.db'
#secret key
app.config['SECRET_KEY'] = "Welcome!"
db = SQLAlchemy(app)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)