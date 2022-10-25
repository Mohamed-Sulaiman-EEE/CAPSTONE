from multiprocessing.sharedctypes import Value
from time import time
from unicodedata import name
from flask import Blueprint, render_template, request, flash, jsonify , redirect, url_for
from flask_login import login_required, current_user
from .models import  User , Conductor_details , Route, Scratch_card , Site_settings , Helpdesk_recharge, Trip  , Fare
from . import db
import json , requests , random , datetime
import webbrowser
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
        elif card.security_hash != security_hash:
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
    conductor_details = Conductor_details.query.filter_by(conductor_id = current_user.id).first()
    return render_template("conductor_home.html" , user = current_user,cd = conductor_details)



@views.route('/conductor-current-trip', methods=['GET', 'POST'])
@login_required
def conductor_current_trip ():
    conductor_details = Conductor_details.query.filter_by(conductor_id = current_user.id).first()
    if conductor_details.current_trip_id :
        trip = Trip.query.filter_by(trip_id= conductor_details.current_trip_id).first()
        route = Route.query.filter_by(route_id = trip.route_id ).first()


        if request.method=="POST":
            passenger_account_number = request.form.get('account_number')
            destination_stop = request.form.get('to')
            no = int(request.form.get('no'))
            def generate_fare(route = route , trip = trip ):
                data = route.start +"," + route.stops + "," + route.end
                data = data.split(",")
                curr_stop = trip.current_stop
                curr_index = 0
                dest_index = 0
                for i in range(len(data)):
                    if data[i] == curr_stop:
                        curr_index = i
                    if data[i] == destination_stop:
                        dest_index = i
                fare = 0
                while curr_index != dest_index:
                    next_stop = data[curr_index+1]
                    sprint = Fare.query.filter_by(from_=curr_stop , to = next_stop).first()
                    if sprint :
                        fare = fare + sprint.price
                        curr_index +=1
                        curr_stop = data[curr_index]
                flash(fare)
                return fare

            fare = generate_fare(route = route , trip = trip )
            fare = fare*no
            flash(fare)


        return render_template("conductor_current_trip.html" , user = current_user , cd=conductor_details ,trip = trip ,route=route)
    
    

        

        
    
    
    return render_template("conductor_current_trip.html" , user = current_user, cd = conductor_details)



@views.route('/conductor-my-trips', methods=['GET', 'POST'])
@login_required
def conductor_my_trips():
    trips = Trip.query.filter_by(conductor_id = current_user.id).all()
    conductor_details = Conductor_details.query.filter_by(conductor_id = current_user.id).first()
    return render_template("conductor_my_trips.html" , user = current_user , trips = trips, cd= conductor_details )



@views.route('/conductor-view-details/<trip_id>', methods=['GET', 'POST'])
@login_required
def conductor_view_details (trip_id):
    trip = Trip.query.filter_by(trip_id=trip_id).first()
    route = Route.query.filter_by(route_id = trip.route_id ).first()
    #tickets = trip.tickets
    return render_template("conductor_view_details.html" , user = current_user, trip=trip, route=route )


@views.route('/conductor-utility-create-trip/<route_id>', methods=['GET' , 'POST'])
@login_required
def conductor_utility_create_trip(route_id):
    conductor_details = Conductor_details.query.filter_by(conductor_id = current_user.id).first()
    if conductor_details.current_trip_id is not None:
        flash("Complete the present trip !!!")
        return render_template("conductor_home.html" , user = current_user,cd = conductor_details)
    route = Route.query.filter_by(route_id = route_id).first()
    date_time = datetime.datetime.now()
    date = str(date_time.strftime('%x'))
    start_time = str(date_time.strftime('%X'))
    end_time="XX:XX:XX"
    trip = Trip(route_id= route_id ,
                conductor_id = current_user.id , 
                collection = 0,
                ticket_run =0,
                status = "A",
                current_passengers = 0,
                current_stop = route.start,
                date = date ,
                start_time = start_time,
                end_time = end_time ,
                bus_no = conductor_details.bus_no,
                gps = "LAT,LON")
    db.session.add(trip)
    db.session.commit()
    conductor_details.current_trip_id = trip.trip_id
    db.session.commit()
    flash("Trip created succesfully ")
    return redirect(url_for('views.conductor_current_trip'))
    


@views.route('/conductor-utility-end-trip/<trip_id>', methods=['GET' , 'POST'])
@login_required
def conductor_utility_end_trip(trip_id):
    conductor_details = Conductor_details.query.filter_by(conductor_id = current_user.id).first()
    if conductor_details.current_trip_id is not None:
        conductor_details.current_trip_id = None
        trip = Trip.query.filter_by(trip_id = trip_id).first()
        trip.status ="I"
        end_time = str(datetime.datetime.now().strftime("%X"))
        trip.end_time = end_time
        db.session.commit()
        flash("Trip ended Successfully !!! ")
        return render_template("conductor_home.html" , user = current_user,cd = conductor_details)
    return redirect(url_for('views.conductor_current_trip'))


@views.route('/conductor-utility-refresh-gps', methods=['POST'])
def conductor_utility_refresh_gps():
    data = json.loads(request.data);
    gps = data["gps"]    
    cd = Conductor_details.query.filter_by(conductor_id = current_user.id).first()
    trip_id = cd.current_trip_id
    trip = Trip.query.filter_by(trip_id = trip_id).first()
    trip.gps = gps
    db.session.commit()
    return jsonify({})





@views.route('/utility-view-map/<trip_id>', methods=['GET' , 'POST'])
@login_required
def utility_view_map(trip_id):
    trip = Trip.query.filter_by(trip_id = trip_id).first()
    gps = trip.gps
    #base_url = "https://www.google.com/maps/@?api=1&map_action=map&cenetr=" //Without Pointer
    base_url = "https://www.google.com/maps/search/?api=1&query=" # with Pointer
    url = base_url +gps
    webbrowser.open_new(url)
    return redirect(url_for('views.conductor_current_trip'))
    

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




@views.route('/camera', methods=['GET', 'POST'])
def camera():
    return render_template("camera.html" )








@views.route('/test-js', methods=['POST'])
def test_js():
    data = json.loads(request.data)
    gps = data["gps"]
    flash(gps)
    return jsonify({})

