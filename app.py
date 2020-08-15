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


# renders the main page
@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    tasks = list(mongo.db.tasks.find())
    return render_template("tasks.html", tasks=tasks)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists
        existing_user = mongo.db.user_registration.find_one(
            {"username_reg": request.form.get("username_reg").lower()})

        if existing_user:
            flash("username already exists")
            return redirect(url_for("register"))

        register = {
            "username_reg": request.form.get("username_reg").lower(), "password_reg": generate_password_hash(request.form.get("password_reg"))
        }
        mongo.db.user_registration.insert_one(register)

        # put the new user into 'session' cookie
        session["user_registration"] = request.form.get("username_reg").lower()
        flash("Registration successful")
        return redirect(url_for("profile", username_reg=session["user_registration"]))
    return render_template("register.html")


@ app.route("/logout")
def logout():
    # remove user form session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# User sign in
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # check if username exists in DB
        existing_user = mongo.db.username_reg.find_one(
            {"username_reg": request.form.get("username_reg").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(existing_user["password_reg"], request.form.get("password_reg")):
                session["username_reg"] = request.form.get(
                    "username_reg").lower()
                flash("Welcome, {}".format(
                    request.form.get("username_reg")))
                return redirect(url_for("profile", username=session["username_reg"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("signin"))
        else:
            # username doesn't exist
            flash("Incorrect username and/or password")
            return redirect(url_for("signin"))

    return render_template("signin.html")


@ app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        is_urgent = "on" if request.form.get("is_urgen") else "off"
        task = {
            "category_name": request.form.get("category_name"),
            "task_name": request.form.get("task_name"),
            "task_description": request.form.get("task_description"),
            "is_urgen": is_urgent,
            "due_date": request.form.get("due_date"),
            "created_by": session["user"]
        }
        mongo.db.tasks.insert_one(task)
        flash("Task successfully added")
        return redirect(url_for("get_tasks"))
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_task.html", categories=categories)


@app.route("/profile")
def profile_page():
    return render_template("profile.html")


# @ app.route("/profile/<username_reg>", methods=["GET", "POST"])
# def profile(username_reg):
#     # Grabs the sessions user's username from DB
#     username_reg = mongo.db.username_reg.find_one(
#         {"username_reg": session["username_reg"]})["username_reg"]
#     if session["username_reg"]:
#         return render_template("profile.html", username_reg=username_reg)
#     return redirect(url_for("signin"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
