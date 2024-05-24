from flask import Flask, render_template, request, redirect, url_for
import json
#import FlightList
import static.py.bookingList 

app = Flask(__name__)

with open('static/json/FlightList.json', 'r') as file:
    flights = json.load(file)
    
with open('static/json/MenuList.json', 'r') as file:
    MenuList = json.load(file)
    
@app.route('/')
def home():
    return render_template('Website.html', flights=flights)

@app.route('/booking', methods=['GET'])
def booking():
    if request.method == 'GET':
        flightId = request.args.get('flight_id')
        
        return render_template('booking.html', flights=flights, flightId=flightId)

@app.route('/drinks')
def drinksandmenu():
    return render_template('drinksandmenu.html', menu=MenuList)

@app.route('/flights')
def flightpage():
    return render_template('flights.html', flights=flights)


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['firstName']
    lname = request.form['lastName']
    seats = request.form["seatsVar"]
    BookingId = request.form["BookingId"]
    flightId = request.form["flightID"]
    
    li = list(seats.split(","))

    updateBooking(flightId, BookingId, name, lname, li)
    
    # Here you can process the form data, such as saving it to a file or database
    return redirect(url_for('home'))

def updateBooking(flightID, bookingID, name, lname, seats):
    content = {
        "flightID": flightID,
        "customer": {
            "firstName": name,
            "lastName": lname
        },
        "bookingID": bookingID,
        "planeSeat": seats,
        "food": []
    }


    # Load existing data from the file
    with open("static/py/bookingList.py", 'r') as file:
        existing_data = json.load(file)

    # Append the new data to the existing list
    existing_data["booking"].append(content)

    # Write the updated list back to the file
    with open("static/py/bookingList.py", 'w') as file:
        json.dump(existing_data, file, indent=4)

@app.route('/updateDrinks', methods=['POST'])
def updateDrinks():       
    bookingID = request.form['BookingID'] 
    order = request.form['oooohImHidden']   

    print(order)

    print(f"Received Booking ID: {bookingID}")
    print(f"Received Order: {order}")

    with open("static/py/bookingList.py", 'r') as file:
        book = json.load(file)
    
    for x in book['booking']:
        if bookingID == x['bookingID']:
            li = list(order.split(","))
            for item in li:
                x['food'].append(item)
                print(item)
                
    with open("static/py/bookingList.py", 'w') as file:
        json.dump(book, file, indent=4)
         
    return redirect(url_for('home'))

@app.route('/manage')
def manage():
    return render_template('login.html')

with open('static/py/bookingList.py', 'r') as file:
    booking = json.load(file)

@app.route('/flightmanage', methods=['POST'])
def flightmanage():

        BookingId = request.form["bookingId"]
        for x in booking["booking"]:
            if x["bookingID"] == BookingId:
                flight = x["flightID"]
                name = x["customer"]["firstName"]
                seat = x["planeSeat"]
                food = x["food"]
                for j in flights["flightData"]:
                    if j["flightID"] == flight:
                        time = j["departure"]["time"]
                        return render_template('hometest.html', flight=flight, name=name, seat=seat, food=food, time=time, booking=booking)
                # If the flight ID is not found in the flight data, set time to "unknown"
                time = "unknown"
        # If no matching booking ID is found, return an appropriate message
        return f"Woah, wait a sec buddy. Is that a real ID? Try again when you're 18 pal {BookingId}"
        

if __name__ == '__main__':
    app.run(debug=True)
