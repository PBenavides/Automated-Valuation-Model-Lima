from webpage import db
## TO DO: Write all the valuation on the database

class House_to_Valuate(db.Model):
    
    id = db.Column(db.Integer(), primary_key=True)

    Barrio = db.Column(db.String()) #Slide
    Ciudad = db.Column(db.String()) #Slide

    Area_total = db.Column(db.Integer(length=3), nullable=False)
    Area_constr = db.Column(db.Integer(length=3), nullable = False)

    NroBanios = db.Column(db.Integer(length=1))
    Dormitorios = db.Column(db.Integer(length=1))

    Antiguedad = db.Column(db.Integer(length=1))
    Cocheras = db.Column(db.Integer(length=1))

    