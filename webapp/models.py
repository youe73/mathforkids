from datetime import datetime
from webapp import db, login_manager
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)    
    password = db.Column(db.String(60), nullable=False)
    registerdate = db.Column(db.DateTime, default=datetime.utcnow())
    registerkids = db.relationship('Registerkids', backref='users', lazy=True)    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Registerkids(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kidsusername = db.Column(db.String(20), unique=True, nullable=False)
    kidspassword = db.Column(db.String(60), nullable=False)
    age = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) #, nullable=False)
    score = db.Column(db.Integer, default=0)
    moduleid = db.relationship('Modules', backref='registerkids', lazy=True)


class Modules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modulename = db.Column(db.String(50))
    assignmentcalc = db.relationship('Assignmentcalc', backref='modules')
    assignmenttext = db.relationship('Assignmenttext', backref='modules')        
    completed_module = db.Column(db.Integer, default=0)    
    registerkids_id = db.Column(db.Integer, db.ForeignKey('registerkids.id')) #, nullable=False)

    def __repr__(self):
        return f"Modules('{self.modulename}')"
    

class Assignmentcalc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field1 = db.Column(db.REAL)
    operator = db.Column(db.String(10))
    field2 = db.Column(db.REAL)
    result = db.Column(db.REAL)
    initiated_assignment = db.Column(db.Integer, default=0)
    completed_assignment = db.Column(db.Integer, default=0)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id')) #, nullable=False)

    def __repr__(self):
        return f"Assignmentcalc('{self.field1, self.operator, self.field2}')"
    
class Assignmenttext(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.Text)
    result = db.Column(db.REAL)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id')) #, nullable=False)

"""
class Kidsassignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kidsmodule = db.Column(db.Integer)
    

"""
   