from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,Email,EqualTo,DataRequired


class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Signup')

class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')
