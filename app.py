import os
from flask import (Flask, flash, render_template,
                   redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.message import EmailMessage
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')


mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    return render_template("main.html", title='oneHourmaid')


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/cleaner_account")
def cleaner_account():
    basic_clean_details = list(mongo.db.basic_clean_details.find())
    deep_clean_details = list(mongo.db.deep_clean_details.find())
    moving_details = list(mongo.db.moving_details.find())

    return render_template("cleaner_account.html", title='oneHourmaid', basic_clean_details=basic_clean_details,
                           deep_clean_details=deep_clean_details)


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
        details = mongo.db.basic_clean_details.insert_one(basic_clean_details)
        flash("Request sent to cleaner")
        send_email(request.form.get("user_email"))
        return redirect(url_for("basic_clean_info_details", request_id=details.inserted_id))
    return render_template("basic_clean_info.html", title='Request Details')


@app.route("/basic_clean_info/<request_id>", methods=["GET", "POST"])
def basic_clean_info_details(request_id):
    details = list(mongo.db.basic_clean_details.find(
        {"_id": ObjectId(request_id)}))
    return render_template("basic_clean_details.html", basic_clean_details=details[0], title='Request Details')


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
        mongo.db.basic_clean_details.update(
            {"_id": ObjectId(request_id)}, submit_basic_clean_details)
        flash("Request Updated!")
        return redirect(url_for("basic_clean_info"))

    request_info = mongo.db.basic_clean_details.find_one(
        {"_id": ObjectId(request_id)})
    return render_template("edit_request.html", request=request_info)


@app.route("/delete_request/<request_id>")
def delete_request(request_id):
    mongo.db.basic_clean_details.remove({"_id": ObjectId(request_id)})
    flash("Request Deleted")
    return redirect(url_for('basic_clean_info'))


# Auto email to send confirmation to user
def send_email(user_email):
    msg = EmailMessage()
    msg['Subject'] = 'oneHourmaid, Cleaner Confirmed!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = user_email

    msg.set_content('This is a plain text email')

    msg.add_alternative("""\
    <!DOCTYPE html>
    <html lang="en">
    <head>
    </head>
    <body>
        <h1 style="text-align: center;">Request Accepted! </h1>
        <p style="text-align: center;">Your cleaner will be with you on your requested date!<br><br>
            <small style="text-align: center; text-decoration: underline;">If you have any questions, feel free to respond to this email</small>
        </p>
    </body>
    </html>
    """, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


@app.route("/auto_email")
def auto_email():
    msg = EmailMessage()
    msg['Subject'] = 'oneHourmaid, Cleaner Confirmed!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    msg.set_content('This is a plain text email')

    msg.add_alternative("""\
    <!DOCTYPE html>
    <html lang="en">
    <head>
    </head>
    <body>
        <h1 style="text-align: center;">Request Accepted! </h1>
        <p style="text-align: center;">Your cleaner will be with you on your requested date!<br><br>
            <small style="text-align: center; text-decoration: underline;">If you have any questions, feel free to respond to this email</small>
        </p>
    </body>
    </html>
    """, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        flash("Confirmation sent to customer")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
