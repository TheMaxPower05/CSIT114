from flask import Flask, render_template, request
import json
#import FlightList
import static.py.bookingList 

app = Flask(__name__)

with open('static/json/FlightList.json', 'r') as file:
    flights = json.load(file)
    
with open('static/json/MenuList.json', 'r') as file:
    MenuList = json.load(file)

@app.route('/')
def index():
    return render_template('booking.html', flights=flights)

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
    flightId = 12092
    
    updateBooking(flightId, BookingId, name, lname, seats)
    
    # Here you can process the form data, such as saving it to a file or database
    return f"Received data: Name - {name}, Email - {lname}, seats = {seats} BookingID = {BookingId}"

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

if __name__ == '__main__':
    app.run(debug=True)
