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

@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Address Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, addresses=result)


@app.route('/view/<int:address_id>', methods=['GET'])
def record_view(address_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses WHERE id=%s', address_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', city=result[0])


@app.route('/edit/<int:address_id>', methods=['GET'])
def form_edit_get(address_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses WHERE id=%s', address_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', address=result[0])


@app.route('/edit/<int:address_id>', methods=['POST'])
def form_update_post(address_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fName'), request.form.get('lName'), request.form.get('Address'),
                 request.form.get('City'), request.form.get('State'), request.form.get('Zip'), address_id)
    sql_update_query = """UPDATE addresses t SET t.fName = %s, t.lName = %s, t.Address = %s, t.City = 
    %s, t.State = %s, t.Zip = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/address/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New City Form')


@app.route('/address/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fName'), request.form.get('lName'), request.form.get('Address'),
                 request.form.get('City'), request.form.get('State'),
                 request.form.get('Zip'))
    sql_insert_query = """INSERT INTO addresses (fName,lName,Address,City,State,Zip) VALUES (%s, %s,%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:address_id>', methods=['POST'])
def form_delete_post(address_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM addresses WHERE id = %s """
    cursor.execute(sql_delete_query, address_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/addresses', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/addresses/<int:address_id>', methods=['GET'])
def api_retrieve(address_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses WHERE id=%s', address_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/addresses', methods=['POST'])
def api_add() -> str:
    data = request.json
    cursor = mysql.get_db().cursor()
    inputData = (data['fName'], data['lName'], data['Address'],
                 data['City'], data['State'], data['Zip'])
    sql_insert_query = """INSERT INTO addresses (fName,lName,Address,City,State,Zip) VALUES (%s, %s,%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/addresses/<int:address_id>', methods=['PUT'])
def api_edit(address_id) -> str:
    cursor = mysql.get_db().cursor()
    data = request.json
    inputData = (data['fName'], data['lName'], data['Address'],
                 data['City'], data['State'],
                 data['Zip'], address_id)
    sql_update_query = """UPDATE addresses t SET t.fName = %s, t.lName = %s, t.Address = %s, t.City = %s, t.State = %s, t.Zip = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/addresses/<int:address_id>', methods=['DELETE'])
def api_delete(address_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM addresses WHERE id = %s """
    cursor.execute(sql_delete_query, address_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)