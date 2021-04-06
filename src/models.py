from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id
           
        }


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    favorites = db.relationship(Favorites)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            

            

            
        }



class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False) 
    gender = db.Column(db.String(50), nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)  
    eye_color = db.Column(db.String(50), nullable=False)  
    heigth =  db.Column(db.Integer, nullable=False)  
    birth_year = db.Column(db.String(50), nullable=False)
    skin_color = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender ,  
            "hair_color": self.hair_color ,
            "eye_color": self.eye_color ,
            "heigth": self.heigth ,
            "birth_year": self.birth_year ,
            "skin_color": self.skin_color 


        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    diameter =  db.Column(db.Integer, nullable=False)
    orbital_period = db. Column(db.Integer, nullable=False)
    rotation_period =  db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain ,
            "climate": self.climate ,
            "diameter": self.diameter ,
            "orbital_period": self.orbital_period ,
            "rotation_period": self.rotation_period ,
            "population": self.population
           
        }