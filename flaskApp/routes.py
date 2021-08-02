from flask import Blueprint

route_path = Blueprint('route_path', __name__)

#view all records
@route_path.route('/', methods=['GET'])
def index():
    from models import address
    from flask import render_template
    addresses = address.query.all()
    return render_template('index.html', title='Home', addresses=addresses)

#single record view
@route_path.route('/view/<int:address_id>', methods=['GET'])
def record_view(address_id):
    from models import address
    from flask import render_template
    addresses = address.query.get(address_id)
    return render_template('view.html', title='View Form', addresses=addresses)

#edit page
@route_path.route('/edit/<int:address_id>', methods=['GET'])
def form_edit_get(address_id):
    from models import address
    from flask import render_template
    from forms import AddressForm
    formObject = AddressForm()
    addresses = address.query.get(address_id)
    return render_template('edit.html', title='Edit Form', formObject=formObject, addresses=addresses)

#address' being edited
@route_path.route('/edit/<int:address_id>', methods=['POST'])
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
def form_insert_get():
    from flask import render_template
    from forms import AddressForm
    formObject = AddressForm()
    return render_template('new.html', title='New City Form', formObject=formObject)

#process of inserting new address
@route_path.route('/address/new', methods=['POST'])
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

