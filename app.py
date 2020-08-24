import os
from flask import (Flask, flash, render_template,
                   redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
# from twilio.rest import Client
# from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/index")
def index():
    return render_template("main.html")


@app.route("/cleaner_chat")
def cleaner_chat():
    return render_template("chat_page.html")


@app.route("/")
def get_details():
    user_details = list(mongo.db.user_details.find())
    return render_template("main.html", user_details=user_details)


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # Grab the session user's username from DB
    username = mongo.db.registration_details.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)
    return redirect(url_for("signin"))


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
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/signin_page")
def signin_page():
    return render_template("signin.html")


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
                    "profile", username=session["user"]))

            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("signin"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("signin"))

    return render_template("profile.html")


# @app.route("/send_message")
# def send_message():
#     render_template("chat_page.html")
#     account_sid = os.environ["TWILIO_ACCOUNT_SID"]
#     auth_token = os.environ["TWILIO_AUTH_TOKEN"]

#     client = Client(account_sid, auth_token)

#     client.messages.create(
#         to=os.environ["MY_PHONE_NUMBER"],
#         from_="+447576111597",
#         body="Hi!"
#     )

#     return render_template("chat_page.html")


@app.route("/signout")
def signout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user", ["default"])
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
