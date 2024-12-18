### Consolidated and Corrected Code

#### `sqlQueries.py`
import random
import mysql.connector
from db_config import get_connection

# Get a connection to the database
mydb = get_connection()

# Generate unique IDs
def generateid():
    return random.randint(11111, 99999)

# Retrieve the number of passengers from a booking
def book_passengers(bookid):
    mycursor = mydb.cursor()
    sql = "SELECT passengers FROM booking WHERE booking_id = %s"
    mycursor.execute(sql, (bookid,))
    return mycursor.fetchone()[0]

# Retrieve the number of seats left on a bus
def get_bus_seats(busid):
    mycursor = mydb.cursor()
    sql = "SELECT capacity FROM bus WHERE busid = %s"
    mycursor.execute(sql, (busid,))
    return mycursor.fetchone()[0]

# Update the number of seats left after booking
def update_bus_passengers(busid, passengers):
    mycursor = mydb.cursor()
    sql = "UPDATE bus SET capacity = capacity - %s WHERE busid = %s"
    mycursor.execute(sql, (passengers, busid))
    mydb.commit()

# Fetch buses from one location to another
def allbus(to_, from_):
    mycursor = mydb.cursor()
    sql = "SELECT busid, from_, to_, cost, rating, departure, arrival, capacity, date_ FROM bus WHERE to_ = %s AND from_ = %s"
    mycursor.execute(sql, (to_, from_))
    return mycursor.fetchall()

# Fetch detailed information about a specific bus
def busdetails(busid):
    mycursor = mydb.cursor()
    sql = "SELECT busid, from_, to_, cost, rating, departure, arrival, capacity, date_ FROM bus WHERE busid = %s"
    mycursor.execute(sql, (busid,))
    return mycursor.fetchall()

# Insert a new user
def userinsert(details):
    mycursor = mydb.cursor()
    sql = "INSERT INTO user (userid, username, phone, email, bookid) VALUES (%s, %s, %s, %s, %s)"
    mycursor.execute(sql, details)
    mydb.commit()

# Insert a new booking
def bookinginsert(details):
    mycursor = mydb.cursor()
    sql = "INSERT INTO booking (booking_id, userid, busid, passengers, date_) VALUES (%s, %s, %s, %s, %s)"
    mycursor.execute(sql, details)
    mydb.commit()

# Retrieve booking details
def booking_details(booking_id):
    mycursor = mydb.cursor()
    sql1 = "SELECT * FROM booking WHERE booking_id = %s"
    mycursor.execute(sql1, (booking_id,))
    booking_info = mycursor.fetchall()

    sql2 = "SELECT * FROM user WHERE userid IN (SELECT userid FROM booking WHERE booking_id = %s)"
    mycursor.execute(sql2, (booking_id,))
    user_info = mycursor.fetchall()

    sql3 = "SELECT * FROM bus WHERE busid IN (SELECT busid FROM booking WHERE booking_id = %s)"
    mycursor.execute(sql3, (booking_id,))
    bus_info = mycursor.fetchall()

    return booking_info + user_info + bus_info

# Delete a booking
def delete(booking_id):
    det = booking_details(booking_id)
    user_id = det[0][1]

    mycursor = mydb.cursor()
    sql1 = "DELETE FROM booking WHERE booking_id = %s"
    mycursor.execute(sql1, (booking_id,))
    sql2 = "DELETE FROM user WHERE userid = %s"
    mycursor.execute(sql2, (user_id,))
    mydb.commit()

# Update user and booking details
def updatebookuser(user_details, booking_details, booking_id):
    mycursor = mydb.cursor()
    sql = "SELECT userid FROM booking WHERE booking_id = %s"
    mycursor.execute(sql, (booking_id,))
    user_id = mycursor.fetchone()[0]

    sql_update_user = "UPDATE user SET username = %s, phone = %s, email = %s WHERE userid = %s"
    mycursor.execute(sql_update_user, (*user_details, user_id))

    sql_update_booking = "UPDATE booking SET passengers = %s WHERE booking_id = %s"
    mycursor.execute(sql_update_booking, (booking_details[0], booking_id))

    mydb.commit()