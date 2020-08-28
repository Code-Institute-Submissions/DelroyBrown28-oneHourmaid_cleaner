import os
from flask import (Flask, flash, render_template,
                   redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
socketio = SocketIO(app)


@app.route("/")
def get_details():
    user_details = list(mongo.db.user_details.find())
    return render_template("main.html", user_details=user_details)


@app.route("/user_main")
def user_main():
    return render_template("user_main.html")


@app.route("/index")
def index():
    return render_template("main.html")


@app.route("/cleaner_chat")
def cleaner_chat():
    return render_template("chat_page.html")


@socketio.on("my event")
def handle_my_custom_event(json):
    print("received something: " + str(json))
    socketio.emit("my response", json)


@app.route("/signin_page")
def signin_page():
    return render_template("signin.html")


@app.route("/user_chat_page")
def user_chat_page():
    return render_template("user_chat.html")


@app.route("/profile_page/<username>", methods=["GET", "POST"])
def profile_page(username):
    user_details = list(mongo.db.user_details.find())
    # Grab the session user's username from DB
    username = mongo.db.registration_details.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", user_details=user_details, username=username)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username from form already exists in DB
        existing_user = mongo.db.registration_details.find_one(
            {"username": request.form.get("username_reg").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username_reg").lower(),
            "password": generate_password_hash(request.form.get("password_reg"))
        }
        mongo.db.registration_details.insert_one(register)

        # put new user in to session cookie
        session["user"] = request.form.get("username_reg").lower()
        flash("Registration successful")
        return redirect(url_for("signin_page", username=session["user"]))

    return render_template("register.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # check if username exists in DB
        existing_user = mongo.db.registration_details.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()

                return redirect(url_for(
                    "profile_page", username=session["user"]))

            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("signin"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("signin"))

    return redirect(url_for("signin"))


@app.route("/send_info", methods=["GET", "POST"])
def send_info():
    if request.method == "POST":
        user_details = {
            "user_name": request.form.get("user_name"),
            "user_lname": request.form.get("user_lname"),
            "user_contact": request.form.get("user_contact"),
            "user_street": request.form.get("user_street"),
            "user_postcode": request.form.get("user_postcode"),
            "user_message": request.form.get("user_message"),
            "user_date": request.form.get("user_date"),
        }
        mongo.db.user_details.insert_one(user_details)
        flash("Request sent to cleaner")
        return redirect(url_for("send_info"))
    details = mongo.db.user_details.find().sort("category_name", 1)
    return render_template("customer_details.html", user_details=details)


@app.route("/edit_request/<request_id>", methods=["GET", "POST"])
def edit_request(request_id):
    request = mongo.db.user_details.find_one({"_id": ObjectId(request_id)})
    details = mongo.db.user_details.find().sort("user_details", 1)
    return render_template("edit_customer_details.html", details=request)


@app.route("/signout")
def signout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user", ["default"])
    return redirect(url_for("index"))


if __name__ == "__main__":
    socketio.run(app, debug=True)
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
