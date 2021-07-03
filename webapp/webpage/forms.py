from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, SelectField
from wtforms.widgets.core import Select
from webpage.utils import dict_encoder_classes

"""
TO DO:
- importar los choices desde el .pkl. 
- Agregar Validators
"""
dict_encoders_list = dict_encoder_classes()

class ValuationForm(FlaskForm):
    
    #id = db.Column(db.Integer(), primary_key=True)

    Barrio = SelectField(label='Barrio', choices=[(elem,elem) for elem in dict_encoders_list['Barrio']])
    Ciudad = SelectField(label='Ciudad', choices = [(elem,elem) for elem in dict_encoders_list['Ciudad']])


    Area_total = IntegerField(label='Total Area')

    Area_constr = IntegerField(label='Constructed Area')

    NroBanios = SelectField(label='Banios', choices = [('1',1), ('2','2'), ('3','3'), ('4','4')])

    Dormitorios = SelectField(label='Dormitorios', choices = [('1','1'), ('2','2'), ('3','3'), ('4','4')])

    Antiguedad = SelectField(label='Antiguedad', choices = [('1','1'), ('2','2'), ('3','3'), ('4','4')])
    
    Cocheras = SelectField(label='Cocheras', choices = [('1','1'), ('2','2'), ('3','3'), ('4','4')])

    Latitud = FloatField(label='Latitud')
    Longitud = FloatField(label='Longitud')

    submit = SubmitField(label='Predict')