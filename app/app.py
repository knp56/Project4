import mysql.connector
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///addressData.db'
#secret key
app.config['SECRET_KEY'] = "Welcome!"
db = SQLAlchemy(app)





if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)