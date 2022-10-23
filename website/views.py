from multiprocessing.sharedctypes import Value
from unicodedata import name
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import  User , Conductor_details , Route, Scratch_card , Site_settings , Helpdesk_recharge, Trip
from . import db
import json , requests , random , datetime

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
        elif card.security_has != security_hash:
            flash("Wrong security hash !!!",category="error")
        card.status = "U"
        card.user_id = current_user.id
        date = datetime.datetime.now()
        date = str(date.strftime("%c"))
        card.date = date
        current_user.balance += card.value
        db.session.commit()
        flash("{0} Rupess recharged  successfully !!!".format(card.value) , category="success")
    history = current_user.scratch_cards
    help = current_user.helpdesk_recharges
    return render_template("user_wallet.html" , user = current_user , history=history , help = help )

#.................................CONDUCTOR FUNCTIONS .............................................

@views.route('/conductor-home', methods=['GET', 'POST'])
@login_required
def conductor_home():
    route = Route.query.all()
    return render_template("conductor_home.html" , user = current_user,route=route)

@views.route('/conductor-current-trip', methods=['GET', 'POST'])
@login_required
def conductor_current_trip ():
    return render_template("conductor_current_trip.html" , user = current_user)

@views.route('/conductor-my-trips', methods=['GET', 'POST'])
@login_required
def conductor_my_trips():
    trips = Trip.query.filter_by(conductor_id = current_user.id).all()
    return render_template("conductor_my_trips.html" , user = current_user , trips = trips )

@views.route('/conductor-view-tickets/<trip_id>', methods=['GET', 'POST'])
@login_required
def conductor_view_tickets (trip_id):
    flash(trip_id)
    trip = Trip.query.filter_by(trip_id=trip_id).first()
    return render_template("conductor_view_tickets.html" , user = current_user, trip_id = trip_id, trip=trip )




#...................................ADMI FUNCTIONS.................................................

@views.route('/admin-home', methods=['GET', 'POST'])
@login_required
def admin_home():
    return render_template("admin_home.html" , user = current_user )

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
    ss= Site_settings.query.first()
    scr = ss
    if request.method== "POST":
        no = request.form.get('no') 
        value = request.form.get('value')
        account_number = request.form.get('account_number')
        val = request.form.get('val')
        if account_number and val :
            flash("Recharged successfully ")
            val = int(val)
            user = User.query.filter_by(account_number=account_number).first()
            date = datetime.datetime.now()
            date = str(date.strftime("%c"))
            help = Helpdesk_recharge(account_number = user.account_number , value = val , date = date)
            user.balance = user.balance + val
            db.session.add(help)
            db.session.commit()
            passenger = user

            return render_template("admin_wallet_recharge.html" , user = current_user , scr = scr,passenger=passenger)

        if no and value :
            no = int(no)
            value= int(value)
            ss= Site_settings.query.all()
            scr = ss[0].scratch_card_run
            
            for i in range(1, no+1):
                card_num = scr + i
                security_hash =random.randint(10000 , 99999)
                card = Scratch_card(card_number = card_num , security_hash=security_hash , value = value , status = "N" ,user_id = current_user.id)
                db.session.add(card)
                db.session.commit()
                if i == no:
                    ss[0].scratch_card_run = i + scr  
                    db.session.commit()
            flash("Cards generated successfully !!!")
    
    return render_template("admin_wallet_recharge.html" , user = current_user , scr = scr)