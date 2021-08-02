flaskApp->forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class AddressForm(FlaskForm):
    fName = StringField("First Name")
    lName = StringField("Last Name")
    Address = StringField("Address")
    City = StringField("City")
    State = StringField("State")
    Zip = StringField("Zip Code")
    submit = SubmitField("Submit")