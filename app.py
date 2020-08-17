import os
from flask import (Flask, flash, render_template,
                   redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_details")
def get_details():
    user_details = mongo.db.user_details.find()
    return render_template("profile.html", user_details=user_details)


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
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
