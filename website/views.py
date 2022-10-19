from unicodedata import name
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json
# END OF IMPORTS
views = Blueprint('views', __name__)
#....................................................................................
@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

#....................................................................................

#.........................USER FUNCTIONS...........................................................
@views.route('/user-home', methods=['GET', 'POST'])
@login_required
def user_home():
    name = current_user.first_name
    return render_template("user_home.html" , user = current_user, name = name)


@views.route('/user-enquire-route', methods=['GET', 'POST'])
@login_required
def user_enquire_route():
    
    return render_template("user_enquire_route.html" , user = current_user )



@views.route('/user-travel-history', methods=['GET', 'POST'])
@login_required
def user_travel_history():
    return render_template("user_travel_history.html" , user = current_user)



@views.route('/user-wallet', methods=['GET', 'POST'])
@login_required
def user_wallet():
    return render_template("user_wallet.html" , user = current_user)

#.................................CONDUCTOR FUNCTIONS .............................................

@views.route('/conductor-home', methods=['GET', 'POST'])
@login_required
def conductor_home():
    return render_template("conductor_home.html" , user = current_user)

#....................................................................................

@views.route('/admin-home', methods=['GET', 'POST'])
@login_required
def admin_home():
    return render_template("admin_home.html" , user = current_user)
#....................................................................................