from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
# END OF IMPORTS

views = Blueprint('views', __name__)

#....................................................................................
@views.route('/', methods=['GET', 'POST'])

def home():
    
    return render_template("home.html", user=current_user)


#....................................................................................

#....................................................................................
@views.route('/user-home', methods=['GET', 'POST'])
@login_required
def UserHome():
    return render_template("user_home.html" , user = current_user)


#....................................................................................
#....................................................................................

#....................................................................................