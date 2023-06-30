from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    __tablename__ = 'people'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    descripcion = db.Column(db.String(150), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.descripcion = description

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
    
    
class Planet(db.Model):
    __tablename__ = 'planet'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    descripcion = db.Column(db.String(150), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.descripcion = description

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class Favorite(db.Model):
    __tablename__ = 'favorite'
    
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people = db.relationship('People')
    planet = db.relationship('Planet')
    user = db.relationship('User')

    def __init__(self, people_id, planet_id, user_id):
        self.people_id = people_id
        self.planet_id = planet_id
        self.user_id = user_id

    def serialize(self):
        return{
            "id": self.id,
            "people": self.people.serialize() if self.people != None else 'No people',
            "planet": self.planet.serialize() if self.planet != None else 'No planet',
            "user": self.user.serialize() if self.user != None else 'No user'
        }