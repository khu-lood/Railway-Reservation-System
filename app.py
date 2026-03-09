from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import datetime
import random
import os
import time
from mysql.connector import DataError

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Blackstormer@02',
    'database': 'railway'
}

# Fare charges
sleeper_charge = 1.5
third_ac_charge = 2
second_ac_charge = 3
first_ac_charge = 4
current_date = datetime.date.today()
max_date = current_date + datetime.timedelta(days=120)

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/availaible_trains', methods=['GET', 'POST'])
def availaible_trains():
    if request.method == 'POST':
        try:
            start_opt = request.form['from']
            final_opt = request.form['to']
            date = request.form['date']
            
            date_user = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if date_user < current_date or date_user > max_date:
                flash('Please enter a valid date!', 'error')
                return redirect(url_for('availaible_trains'))
            
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT Train_No, Source_Station_Name, Destination_Station_Name, 
                       Arrival_Time, Departure_Time 
                FROM train_info 
                WHERE Source_Station_Code = %s AND Destination_Station_Code = %s
            """
            cursor.execute(query, (start_opt, final_opt))
            result = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return render_template('availaible_trains.html', trains=result)
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('availaible_trains'))
    
    return render_template('availaible_trains_form.html')

@app.route('/check_fare', methods=['GET', 'POST'])
def check_fare():
    if request.method == 'POST':
        try:
            start_opt = request.form['from']
            final_opt = request.form['to']
            
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT Train_No, Distance 
                FROM train_info 
                WHERE Source_Station_Code = %s AND Destination_Station_Code = %s
            """
            cursor.execute(query, (start_opt, final_opt))
            result = cursor.fetchall()
            
            fare_data = []
            for row in result:
                train_no, distance = row
                fare_data.append({
                    'train_no': train_no,
                    'distance': distance,
                    'sleeper': int(distance) * sleeper_charge,
                    'third_ac': int(distance) * third_ac_charge,
                    'second_ac': int(distance) * second_ac_charge,
                    'first_ac': int(distance) * first_ac_charge
                })
            
            cursor.close()
            conn.close()
            
            return render_template('check_fare.html', fares=fare_data)
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('check_fare'))
    
    return render_template('check_fare_form.html')

@app.route('/show_bookings', methods=['GET', 'POST'])
def show_bookings():
    if request.method == 'POST':
        try:
            mobile_no = request.form['mobile']
            
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM bookings WHERE Mobile_No = %s"
            cursor.execute(query, (mobile_no,))
            result = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            if not result:
                flash('No bookings found!', 'info')
                return redirect(url_for('show_bookings'))
            
            return render_template('show_bookings.html', bookings=result)
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('show_bookings'))
    
    return render_template('show_bookings_form.html')

@app.route('/book_train', methods=['GET', 'POST'])
def book_train():
    if request.method == 'POST':
        try:
            train_no = int(request.form['train_no'])
            name = request.form['name']
            mobile = request.form['mobile']
            adhaar = request.form['adhaar']
            travel_class = request.form['class']
            
            # Validate inputs
            if len(name) == 0 or len(name) > 30:
                flash('Please enter a valid name (1-30 characters)', 'error')
                return redirect(url_for('book_train'))
            
            if len(mobile) != 10 or not mobile.isdigit():
                flash('Please enter a valid 10-digit mobile number', 'error')
                return redirect(url_for('book_train'))
            
            if len(adhaar) != 12 or not adhaar.isdigit():
                flash('Please enter a valid 12-digit Aadhaar number', 'error')
                return redirect(url_for('book_train'))
            
            if travel_class not in ['Sleeper', 'AC-1', 'AC-2', 'AC-3']:
                flash('Please select a valid class', 'error')
                return redirect(url_for('book_train'))
            
            # Generate booking ID
            booking_time = datetime.datetime.now()
            booking_id = random.randint(10000, 99999)
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if booking ID is unique
            while True:
                cursor.execute("SELECT Booking_ID FROM bookings WHERE Booking_ID = %s", (booking_id,))
                if cursor.fetchone() is None:
                    break
                booking_id = random.randint(10000, 99999)
            
            # Insert booking
            query = """
                INSERT INTO bookings (Train_No, Passenger_Name, Mobile_No, 
                Passenger_Adhaar, Time_Of_Booking, Booking_ID, Class)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                train_no, 
                name, 
                mobile, 
                adhaar, 
                booking_time, 
                booking_id, 
                travel_class
            ))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            flash('Booking successful! Your Booking ID is: ' + str(booking_id), 'success')
            return redirect(url_for('book_train'))
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('book_train'))
    
    return render_template('book_train_form.html')

@app.route('/cancel_booking', methods=['GET', 'POST'])
def cancel_booking():
    if request.method == 'POST':
        try:
            booking_id = int(request.form['booking_id'])
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if booking exists
            cursor.execute("SELECT * FROM bookings WHERE Booking_ID = %s", (booking_id,))
            booking = cursor.fetchone()
            
            if not booking:
                flash('Booking not found!', 'error')
                return redirect(url_for('cancel_booking'))
            
            # Delete booking
            cursor.execute("DELETE FROM bookings WHERE Booking_ID = %s", (booking_id,))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            flash('Booking cancelled successfully!', 'success')
            return redirect(url_for('cancel_booking'))
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('cancel_booking'))
    
    return render_template('cancel_booking_form.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)