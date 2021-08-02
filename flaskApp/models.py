from app import db


class address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    fName = db.Column(db.String(64), index=False, unique=False, nullable=True)
    lName = db.Column(db.String(80), index=False, unique=False, nullable=True)
    Address = db.Column(db.String(80), index=False, unique=False, nullable=True)
    City = db.Column(db.String(80), index=False, unique=False, nullable=True)
    State = db.Column(db.String(80), index=False, unique=False, nullable=True)
    Zip = db.Column(db.String(80), index=False, unique=False, nullable=True)

    def __init__(self, fName, lName, Address, City, State, Zip):
        #self.id = id
        self.fName = fName
        self.lName = lName
        self.Address = Address
        self.City = City
        self.State = State
        self.Zip = Zip

    #Create a string
    def __repr__(self):
        return '<Name %r>' % self.fName

db.create_all()
