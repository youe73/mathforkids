from flask import Blueprint, render_template, request, url_for, redirect, flash
from webapp.forms import SignupForm, LoginForm
from webapp.models import Users
from webapp import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET', 'POST'])
def login():  
    if current_user.is_authenticated:
        return redirect(url_for('parents.home'))  
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have successfully logged in', 'success')
            return redirect(next_page) if next_page else redirect(url_for('parents.home'))
        else:
            flash('Email and password does not match, please try again', 'danger')
    return render_template('login.html', form = form)

@auth.route('/signup',methods=['GET', 'POST'])
def signup():    
    if current_user.is_authenticated:
        return redirect(url_for('parents.home')) 
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has successfully been created', 'success')

        return redirect(url_for('parents.home'))
    return render_template('signup.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('parents.home'))