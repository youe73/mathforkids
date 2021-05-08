from flask import Blueprint, render_template, request, url_for, redirect
from webapp.forms import KidsLoginForm

kids = Blueprint('kids',__name__)

@kids.route('/kidshome')
def kidshome():
    return render_template('kidshome.html', title='Kids')

@kids.route('/kidslogin')
def kidslogin():
    form = KidsLoginForm()
    return render_template('kidslogin.html',form=form)