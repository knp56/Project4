
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, request, Response, redirect
from routes import route_path
from flask_session import Session
import redis

app = Flask(__name__)
app.register_blueprint(route_path)
#add database

app.secret_key = 'BAD_SECRET_KEY'

# Configure Redis for storing the session data on the server-side
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///addressData.db'
#secret key
app.config['SECRET_KEY'] = "Welcome!"
db = SQLAlchemy(app)

server_session = Session(app)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)