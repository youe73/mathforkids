from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField, IntegerField, FloatField, DecimalField,TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
import email_validator
from webapp.models import db, Users, Assignmentcalc, Modules
import webapp.parents 

class SignupForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username is already taken. Please select a another one')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email is taken. Please select another one')
    

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterKidsForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    age = IntegerField('age', validators=[DataRequired()])
    submit = SubmitField('Register kid')


class KidsLoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])    
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CreateModuleForm(FlaskForm):
    modules = StringField('Module name',validators=[DataRequired()])
    submit = SubmitField('Create Module')   

        
class CreateAssignmentCalculationForm(FlaskForm):
    field1 = FloatField('Field 1', validators=[DataRequired()])    
    operator = SelectField('Operator',choices=[(0,'+'),(1,'-'),(2,'*'),(3,'/')], validators=[DataRequired()])
    field2 = FloatField('Field 2', validators=[DataRequired()])
    submit = SubmitField('Create')
    #submitmodule = SubmitField('Finish and Save')

class CreateAssignmentTextForm(FlaskForm):
    modules = StringField('module',validators=[DataRequired()])
    field = TextAreaField('field', validators=[DataRequired()])    
    result = FloatField('result',validators=[DataRequired()])
    submit = SubmitField('create')


class EditAssignmentCalculationForm(FlaskForm): 
    hiddenid = HiddenField('id')    
    editfield1 = FloatField('editField 1', validators=[DataRequired()])    
    editoperator = SelectField('editOperator',choices=[(0,'+'),(1,'-'),(2,'*'),(3,'/')], validators=[DataRequired()])
    editfield2 = FloatField('editField 2', validators=[DataRequired()])
    submit = SubmitField('Edit')






"""
class KidsassignmentForm(FlaskForm):
    
"""