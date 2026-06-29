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







# run the application
app.run(debug= True)