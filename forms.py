from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import Length,Email,EqualTo,DataRequired
from flask_wtf.file import FileField,FileAllowed,FileRequired


class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=3,max=20)])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Signup')

class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),Length(max=30)])
    Text= TextAreaField('EVERY SPACE IS BATTLE OF IDEOLOGIES,SO WRITE!', render_kw={"rows": 10, "cols": 10},validators=[DataRequired()])
    submit=SubmitField('Post')

class UpdateForm(FlaskForm):
    username=StringField('Change Username',validators=[Length(min=3,max=20)])
    email=StringField('Change Email',validators=[Email()])
    dp=FileField('Change Profile Pic',validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Change')
class UpdatePost(FlaskForm):
    title = StringField('New title', validators=[DataRequired(),Length(max=30)])
    Text= TextAreaField('EDIT POST', render_kw={"rows": 10, "cols": 10},validators=[DataRequired()])
    submit=SubmitField('Update')


