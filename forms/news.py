from unicodedata import category
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired

class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    is_private = BooleanField("Личное")
    category = SelectField("Категория", choices=[], coerce=int)
    submit = SubmitField('Применить')
    
