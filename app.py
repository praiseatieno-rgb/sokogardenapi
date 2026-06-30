# import flask module
from flask import *
import pymysql
#its a python module that enables to create a connection to mysql database

import os


# create an app
app = Flask(__name__)

# below we confirgure where the product image shall be saved
app.config['UPLOAD_FOLDER'] = 'static/images'

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


# create a route that is able to add the products all the way to the data base



@app.route("/api/addproduct", methods=["POST"])
def addproducts():
    if request.method == "POST":
        #get the details passed from the postman
        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        product_cost = request.form["product_cost"]
        product_photo= request.files["product_photo"]
        product_category = request.form["product_category"]

        # since the product is a type of a file, we shall extract the name of the product and that name shall be stored in the data base but the photo product shall be stored into the static/images folder
        filename = product_photo.filename

        # specify where the image will be saved
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # save the image
        product_photo.save(photo_path)

        # create a connection to mysql database by the use of pymysql module
        connection = pymysql.connect(host="localhost", password="",user="root", database="sokogarden")

        #create a cursor
        cursor = connection.cursor()
        
        

        #structure the sql query for insert
        sql = "insert into product_details( product_name, product_description, product_cost, product_photo, product_category) values (%s, %s, %s, %s, %s)"

        # a tuple to hold all  data available on the variables
        data = (product_name, product_description, product_cost, filename, product_category)

        # by use of a cursor, execute the sql query as it replace the placeholder with the actual values
        cursor.execute(sql, data)

        #commit/complete the changes to the database
        connection.commit()

        #give a response to the users
        return jsonify({"message" : "Product added successfully"})







# run the application
app.run(debug= True)