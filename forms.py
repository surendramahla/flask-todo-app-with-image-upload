from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    image = FileField('Add Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Add Task')
