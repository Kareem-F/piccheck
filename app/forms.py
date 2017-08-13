from flask_wtf import FlaskForm 
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
	location = StringField(validators=[DataRequired()])
	img_src  = RadioField('', choices=[('pb', 'Pixabay'), ('fk','Flicker')], default='pb')