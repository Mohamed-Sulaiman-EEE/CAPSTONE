from multiprocessing.sharedctypes import Value
from unicodedata import name
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User , Conductor_details , Route, Scratch_card , Site_settings
from . import db
import json , requests , random
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
    
    return render_template("user_home.html" , user = current_user)


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
    if request.method == "POST":
        id = request.form.get('card_number')
        security_hash = request.form.get('security_hash')
        card = Scratch_card.query.filter_by(card_number = id ).first()
        if card.status == "U":
            flash("Card has already been used !!!" , category="error")
            return render_template("user_wallet.html", user = current_user)
        card.status = "U"
        card.user_id = current_user.id
        current_user.balance += card.value
        db.session.commit()
        flash("{0} Rupess recharged  successfully !!!".format(card.value) , category="success")
    return render_template("user_wallet.html" , user = current_user)

#.................................CONDUCTOR FUNCTIONS .............................................

@views.route('/conductor-home', methods=['GET', 'POST'])
@login_required
def conductor_home():
    data = current_user.conductors
    data = data[0]
    
    
    return render_template("conductor_home.html" , user = current_user, data=data )

#...................................ADMI FUNCTIONS.................................................

@views.route('/admin-home', methods=['GET', 'POST'])
@login_required
def admin_home():

    route = Route.query.all()
    return render_template("admin_home.html" , user = current_user , data=route)
#....................................................................................
@views.route('/admin-manage-routes', methods=['GET', 'POST'])
@login_required
def admin_manage_routes():
    if request.method == "POST":
        route_id =  request.form.get('route_id') 
        start =  request.form.get('start') 
        end =  request.form.get('end') 
        stops =  request.form.get('stops')
        new_route = Route(route_id=route_id , start=start , end = end , stops = stops)
        db.session.add(new_route)
        db.session.commit()
        flash("Route added successfully !!!")
    route = Route.query.all()
    return render_template("admin_manage_routes.html" , user = current_user , route=route)


@views.route('/admin-wallet-recharge', methods=['GET', 'POST'])
@login_required
def admin_wallet_recharge():
    if request.method== "POST":
        sc= Site_settings.query.all()
        scr = sc[0].scratch_card_run
        no = int(request.form.get('no')) 
        value = int(request.form.get('value'))
        for i in range(1, no+1):
            card_num = scr + i
            security_hash =random.randint(10000 , 99999)
            card = Scratch_card(card_number = card_num , security_hash=security_hash , value = value , status = "N" ,user_id = current_user.id)
            db.session.add(card)
            db.session.commit()
            if i == no:
                sc[0].scratch_card_run = i + scr  
                db.session.commit()
        flash("Cards generated successfully !!!")
    route = Route.query.all()
    sc= Site_settings.query.all()
    scr = sc[0]
    return render_template("admin_wallet_recharge.html" , user = current_user , data=route, scr = scr)