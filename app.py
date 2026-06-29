# import flask module
from flask import *
import pymysql
#its a python module that enables to create a connection to mysql database

# create an app
app = Flask(__name__)


# define the signup/register ulr endpoint
@app.route("/api/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        #get the details passed from the postman
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        phone = request.form["phone"]

        # create a connection to mysql database by the use of pymysql module
        connection = pymysql.connect(host="localhost", password="",user="root", database="sokogarden")

        #create a cursor
        cursor = connection.cursor()

        # check if email already exists
        check_sql = "SELECT * FROM users WHERE email = %s"
        cursor.execute(check_sql, (email,))
        user = cursor.fetchone()

        if user:
            return jsonify({
                "message": "already registered"
                })
        
        

        #structure the sql query for insert
        # %s it stands for pre-prepared statement. it is a placeholder that will replace actual values
        sql = "insert into users( username, password, email, phone) values (%s, %s, %s, %s)"

        # create a tuple to hold all your data available on the variables
        data = (username, password, email, phone)

        # by use of a cursor, execute the sql query as you replace the placeholder with the actual values
        cursor.execute(sql, data)

        #commit/complete the changes to the database
        connection.commit()

        #give a response to the users
        return jsonify({"message" : "user registered successfully"})
    
import pymysql.cursors
# below is the sign in api endpoint
@app.route("/api/signin", methods = ["POST"])
def signin():
    if request.method == "POST":
        # extract the data from postman
        email = request.form["email"]
        password = request.form["password"]

        #create a connecton to the DB
        connection = pymysql.connect(host="localhost", password="", user="root", database="sokogarden")

        #create a cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        #structure the sql query to check whether the person trying to login already has an account
        sql = "select * from users where email = %s and password = %s"

        # create a tuple to hold your details
        data = (email, password)

        #by use of cursor, execute the query
        cursor.execute(sql, data)

        # check how many row are returned when the query is executed.
        count = cursor.rowcount

        if count == 0:
            return jsonify({"message" : "Login failed. Please check on the details entered."})
        else:
            # if the user is there, take the details of the user and store them onto a variable and return a message of success to the user.
            user = cursor.fetchone()
            return jsonify({"message" : "Login a success","user": user})







# run the application
app.run(debug= True)