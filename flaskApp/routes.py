from functools import wraps

from flask import Blueprint, session, render_template_string, request, redirect, url_for
from flask_session import Session


route_path = Blueprint('route_path', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('email') is None:
            return redirect('/get_email',code=302)
        return f(*args, **kwargs)
    return decorated_function

#view all records
@route_path.route('/', methods=['GET'])
@login_required
def index():
    from models import address
    from flask import render_template
    addresses = address.query.all()
    return render_template('index.html', title='Home', addresses=addresses)

#single record view
@route_path.route('/view/<int:address_id>', methods=['GET'])
@login_required
def record_view(address_id):
    from models import address
    from flask import render_template
    addresses = address.query.get(address_id)
    return render_template('view.html', title='View Form', addresses=addresses)

#edit page
@route_path.route('/edit/<int:address_id>', methods=['GET'])
@login_required
def form_edit_get(address_id):
    from models import address
    from flask import render_template
    from forms import AddressForm
    formObject = AddressForm()
    addresses = address.query.get(address_id)
    return render_template('edit.html', title='Edit Form', formObject=formObject, addresses=addresses)

#address' being edited
@route_path.route('/edit/<int:address_id>', methods=['POST'])
@login_required
def form_update_post(address_id):
    from models import address
    from flask import request, redirect
    from app import db
    update_this = address.query.get(address_id)
    update_this.fName = request.form.get('fName')
    update_this.lName = request.form.get('lName')
    update_this.Address = request.form.get('Address')
    update_this.City = request.form.get('City')
    update_this.State = request.form.get('State')
    update_this.Zip = request.form.get('Zip')
    db.session.flush()
    db.session.commit()
    return redirect("index.html", code=302)

#new address page
@route_path.route('/address/new', methods=['GET'])
@login_required
def form_insert_get():
    from flask import render_template
    from forms import AddressForm
    formObject = AddressForm()
    return render_template('new.html', title='New City Form', formObject=formObject)

#process of inserting new address
@route_path.route('/address/new', methods=['POST'])
@login_required
def form_insert_post():
    from models import address
    from flask import render_template
    from app import db
    from forms import AddressForm
    formObject = AddressForm()
    insertObject = address(fName = formObject.fName.data,lName = formObject.lName.data ,Address = formObject.Address.data,City = formObject.City.data,State = formObject.State.data,Zip = formObject.Zip.data)
    db.session.add(insertObject)
    db.session.commit()
    return render_template('new.html', title='New City Form', formObject = formObject)

#process of deleting address
@route_path.route('/delete/<int:address_id>', methods=['POST'])
@login_required
def form_delete_post(address_id):
    from flask import redirect
    from models import address
    from forms import AddressForm
    from app import db
    formObject = AddressForm()
    deleteObject = address.query.get(address_id)
    db.session.delete(deleteObject)
    db.session.commit()
    return redirect("/", code=302)

@route_path.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'POST':
        # Save the form data to the session object
        session['email'] = request.form['email_address']
        return redirect(url_for('route_path.get_email'))

    return """
        <form method="post">
            <label for="email">Enter your email address:</label>
            <input type="email" id="email" name="email_address" required />
            <button type="submit">Submit</button
        </form>
        """


@route_path.route('/get_email')
def get_email():
    return render_template_string("""
            {% if session['email'] %}
                <h1>Welcome {{ session['email'] }}!</h1>
            {% else %}
                <h1>Welcome! Please enter your email <a href="{{ url_for('route_path.set_email') }}">here.</a></h1>
            {% endif %}
        """)


@route_path.route('/delete_email')
def delete_email():
    # Clear the email stored in the session object
    session.pop('email', default=None)
    return '<h1>Session deleted!</h1>'


#Postman - all addresses
# @route_path.route('/api/v1/addresses', methods=['GET'])
# def api_browse() -> str:
#
#     resp = Response(json_result, status=200, mimetype='application/json')
#     return resp
#
#
# #Postman - single record
# @route_path.route('/api/v1/addresses/<int:address_id>', methods=['GET'])
# def api_retrieve(address_id) -> str:
#     addresses = address.query.all()
#     format_address = []
#     for a in addresses:
#         #query.filter(address.fName = fName)
#         format_address.append({
#             'id':a.id,
#             'fName':a.fName,
#             'lName':a.lName,
#             'Address':a.Address,
#             'City':a.City,
#             'State':a.State,
#             'Zip':a.Zip
#         })
#     json_result = json.dumps({'addresses':format_address})
#     resp = Response(json_result, status=200, mimetype='application/json')
#     return resp
#
# #Postman - new address
# @route_path.route('/api/v1/addresses', methods=['POST'])
# def api_add() -> str:
#     data = request.json
#     insert_object = address(data['fName'], data['lName'], data['Address'], data['City'], data['State'], data['Zip'])
#     db.session.add(insert_object)
#     db.session.commit()
#     resp = Response(status=201, mimetype='application/json')
#     return resp
#
# #Postman - edit
# @route_path.route('/api/v1/addresses/<int:address_id>', methods=['PUT'])
# def api_edit(address_id) -> str:
#     data = request.json
#     edit_object = address(data['fName'], data['lName'], data['Address'], data['City'], data['State'], data['Zip'])
#     db.session.update(edit_object)
#     db.session.commit()
#     resp = Response(status=200, mimetype='application/json')
#     return resp
#
# #Postman - delete
# @route_path.route('/api/v1/addresses/<int:address_id>', methods=['DELETE'])
# def api_delete(address_id) -> str:
#     data = request.json
#     delete_object = address(data['fName'], data['lName'], data['Address'], data['City'], data['State'], data['Zip'])
#     db.session.delete(delete_object)
#     db.session.commit()
#     resp = Response(status=200, mimetype='application/json')
#     return resp
#

