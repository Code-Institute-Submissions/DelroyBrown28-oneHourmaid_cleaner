import os
from flask import (Flask, flash, render_template,
                   redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_socketio import SocketIO, emit
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    return render_template("main.html", title='oneHourmaid')


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/basic_clean_page")
def basic_clean_page():
    return render_template("basic_clean_details.html")


@app.route("/cleaner_account")
def cleaner_account():
    basic_clean_details = list(mongo.db.basic_clean_details.find())
    deep_clean_details = list(mongo.db.deep_clean_details.find())
    moving_details = list(mongo.db.moving_details.find())

    return render_template("cleaner_account.html", title='oneHourmaid', basic_clean_details=basic_clean_details,
                           deep_clean_details=deep_clean_details)


@app.route("/deep_clean")
def deep_clean():
    return render_template("deep_clean_details.html", title='Deep Clean Request')


@app.route("/moving_in_out")
def moving_in_out():
    return render_template("moving.html", title='Moving In/Out')


@app.route("/reply_to")
def reply_to():
    username = mongo.db.registration_details.find_one(
        {"username": session["user"]})["username"]
    return render_template("reply_to.html", username=username)


# @app.errorhandler(404)
# def invalid_page(e):
#     return render_template("404.html")


@app.route("/profile_page/<username>", methods=["GET", "POST"])
def profile_page(username):
    basic_clean_details = list(mongo.db.basic_clean_details.find())
    deep_clean_details = list(mongo.db.deep_clean_details.find())
    moving_details = list(mongo.db.moving_details.find())
    # Grab the session user's username from DB
    username = mongo.db.registration_details.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", title='oneHourmaid', basic_clean_details=basic_clean_details,
                               moving_details=moving_details, username=username, deep_clean_details=deep_clean_details)


@app.route("/basic_clean_info", methods=["GET", "POST"])
def basic_clean_info():
    if request.method == "POST":
        basic_clean_details = {
            "user_name": request.form.get("user_name"),
            "user_lname": request.form.get("user_lname"),
            "user_contact": request.form.get("user_contact"),
            "user_street": request.form.get("user_street"),
            "user_postcode": request.form.get("user_postcode"),
            "user_message": request.form.get("user_message"),
            "user_date": request.form.get("user_date"),
        }
        mongo.db.basic_clean_details.insert_one(basic_clean_details)
        flash("Request sent to cleaner")
        return redirect(url_for("basic_clean_info"))
    details = mongo.db.basic_clean_details.find().sort("basic_clean_details", 1)
    return render_template("basic_clean_details.html", basic_clean_details=details, title='Request Details')


# @app.route("/view_request/<request_id>", methods=["GET"])
# def view_request(request_id):
#     request_info = mongo.db.basic_clean_details.find_one(
#         {"_id": ObjectId(request_id)})
#     basic_clean_details = list(mongo.db.basic_clean_details.find())

#     return render_template("view_request.html", basic_clean_details=basic_clean_details,
#                            request_id=request_id, title='View Request')


@app.route("/edit_request/<request_id>", methods=["GET", "POST"])
def edit_request(request_id):
    if request.method == "POST":
        submit_basic_clean_details = {
            "user_name": request.form.get("user_name"),
            "user_lname": request.form.get("user_lname"),
            "user_contact": request.form.get("user_contact"),
            "user_street": request.form.get("user_street"),
            "user_postcode": request.form.get("user_postcode"),
            "user_message": request.form.get("user_message"),
            "user_date": request.form.get("user_date"),
        }
        mongo.db.basic_clean_details.update_one(
            {"_id": ObjectId(request_id)}, submit_basic_clean_details)
        flash("Request Updated!")
        return redirect(url_for("basic_clean_info"))

    request_info = mongo.db.basic_clean_details.find_one(
        {"_id": ObjectId(request_id)})
    return render_template("edit_request.html", request=request_info)


@app.route("/deep_clean_info", methods=["GET", "POST"])
def deep_clean_info():
    if request.method == "POST":
        deep_clean_details = {
            "user_name": request.form.get("user_name"),
            "user_lname": request.form.get("user_lname"),
            "user_contact": request.form.get("user_contact"),
            "user_street": request.form.get("user_street"),
            "user_postcode": request.form.get("user_postcode"),
            "user_message": request.form.get("user_message"),
            "user_date": request.form.get("user_date"),
            "carpet_clean": request.form.get("carpet_clean"),
            "floor_steam": request.form.get("floor_steam"),
            "white_goods": request.form.get("white_goods"),
            "window_clean": request.form.get("window_clean"),
        }
        mongo.db.deep_clean_details.insert_one(deep_clean_details)
        flash("Request sent to cleaner")
        return redirect(url_for("deep_clean_info"))
    details = mongo.db.deep_clean_details.find().sort("deep_clean_details", 1)
    return render_template("deep_clean_details.html", deep_clean_details=details, title='Deep Clean Request')


@app.route("/moving_info", methods=["GET", "POST"])
def moving_info():
    if request.method == "POST":
        moving_details = {
            "street_moving": request.form.get("street_moving"),
            "postcode_moving": request.form.get("postcode_moving"),
            "date_moving": request.form.get("date_moving"),
            "name_moving": request.form.get("name_moving"),
            "contact_moving": request.form.get("contact_moving"),
            "moving_in": request.form.get("moving_in"),
            "moving_out": request.form.get("moving_out")
        }
        mongo.db.moving_details.insert_one(moving_details)
        flash("Request sent to cleaner")
        return redirect(url_for("moving_info"))
    details_moving = mongo.db.moving_details.find().sort("moving_details", 1)

    return render_template("moving.html", moving_details=details_moving)


# @app.route("/edit_request/<request_id>", methods=["GET", "POST"])
# def edit_request(request_id):
#     request = mongo.db.user_details.find_one({"_id": ObjectId(request_id)})
#     details = mongo.db.user_details.find().sort("user_details", 1)
#     return render_template("deep_clean_details.html", request=request, details=details)


# @app.route("/edit_request/<request_id>", methods=["GET", "POST"])
# def edit_request(request_id):
#     request = mongo.db.user_details.find_one({"_id": ObjectId(request_id)})
#     return render_template("edit_request.html", request=request)



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
