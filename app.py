from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL 
from random import sample
import ast
import hashlib

from werkzeug.security import check_password_hash, generate_password_hash
from myfunctions import *


# Initial app configuration
app = Flask(__name__)

# Session will use filesystem cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connecting database (SQLite3)
db = SQL("sqlite:///database.db")

@app.route("/")
@login_required
def index():
    
    return render_template("index.jinja-html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Clear current existing session
    session.clear()
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        
        # Ensuring that provided login and password are correct
        if len(user) != 1 or not check_password_hash(user[0]["hash"], password):
            message = "Invalid username and/or password"
            return render_template("login.jinja-html", message=message)
        
        # Remembering user session
        session["user_id"] = user[0]["id"]
        
        # Redirect user to the home page
        return redirect("/")
    
    else:
        return render_template("login.jinja-html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        users = db.execute("SELECT * FROM users WHERE username = ?", str(username))
        
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        message = ""
    
        # Checking inserted data if correct
        if not username:
            message = "Please provide username."
            return render_template("register.jinja-html", message=message)
        elif len(users) != 0 and users[0]["username"] == username:
            message = "Username already taken."
            return render_template("register.jinja-html", message=message)
        elif password != confirmation or not password:
            message = "Insert the passwords and make sure they match"
            return render_template("register.jinja-html", message=message)
        
        # Generating hash from given password and saving it in the database
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        
        # Returning to the home page
        return redirect("/")
    
    # If reached via GET, render register template
    else:
        return render_template("register.jinja-html")
    
@app.route("/logout")
def logout():
    # Logging out the user and redirecting them to the home page
    session.clear()
    return redirect("/")

@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    if request.method == "POST":
        oldpassword = request.form.get("oldpassword")
        confirmation = request.form.get("confirmation")
        newpassword = request.form.get("newpassword")
        currentpassword = db.execute("SELECT hash FROM users WHERE id = ?", session.get("user_id"))
        
        # Checking if the data provided is valid
        if not oldpassword or not newpassword or not confirmation or newpassword != confirmation:
            message = "Please insert passwords and make sure they match."
            return render_template("changepassword.jinja-html", message=message)
            
        elif not check_password_hash(currentpassword[0]["hash"], oldpassword):
            message = "Please insert your current password correctly."
            return render_template("changepassword.jinja-html", message=message)
        
        elif oldpassword == newpassword:
            message = "Please don't use already used password."
            return render_template("changepassword.jinja-html", message=message)
        
        # Hashing new password and replacing the old one with it and redirecting user to the home page
        hash = generate_password_hash(newpassword, method='pbkdf2:sha256', salt_length=8)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, session.get("user_id"))
        
        return redirect("/")

    else:
        return render_template("changepassword.jinja-html")
    
@app.route("/createsurvey", methods=["GET", "POST"])
@login_required
def createsurvey():

    if request.method == "POST":
        # Checking if there is any existing survey
        # If user has no surveys, adding temporary one
        existing = db.execute("SELECT * FROM surveysid WHERE user_id = ? ORDER BY id DESC LIMIT 1", session.get("user_id"))
        if len(existing) == 0:
            db.execute("INSERT INTO surveysid (user_id, hash_id) VALUES (?, ?)", session.get("user_id"), "lkjhgfdsa")
        surveyid = db.execute("SELECT * FROM surveysid WHERE user_id = ? ORDER BY id DESC LIMIT 1", session.get("user_id"))[0]["id"]
        surveyid = surveyid + 1
        # Hashing the ID; a hash will be the key to access the survey from outside
        surveyid = str(surveyid)
        hashed_surveyid = hashlib.shake_256(surveyid.encode("utf-8")).hexdigest(4)
        
        # Adding survey ID and hashed survey ID to the database
        db.execute("INSERT INTO surveysid (user_id, hash_id) VALUES (?, ?)", session.get("user_id"), hashed_surveyid)
        
        # Deleting the temporary survey
        db.execute("DELETE FROM surveysid WHERE user_id = ? AND hash_id = ?", session.get("user_id"), "lkjhgfdsa")
        
        # Getting factors' names and their values
        # Price
        priceyou = request.form.get("priceyou")
        pricecomp = request.form.get("pricecomp")
        # Factor no. 2
        factor2_name = request.form.get("_name2")
        factor2_youvalue = request.form.get("factor2_youvalue")
        factor2_compvalue = request.form.get("factor2_compvalue")
        # Factor no. 3
        factor3_name = request.form.get("_name3")
        factor3_youvalue = request.form.get("factor3_youvalue")
        factor3_compvalue = request.form.get("factor3_compvalue")
        
        # Adding all the factors' names and their values to the database
        db.execute("INSERT INTO surveydetails (priceyou, pricecomp, factor2_name, factor2_youvalue, factor2_compvalue, factor3_name, factor3_youvalue, factor3_compvalue, hash_id, survey_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", priceyou, pricecomp, factor2_name, factor2_youvalue, factor2_compvalue, factor3_name, factor3_youvalue, factor3_compvalue, hashed_surveyid, surveyid)
        
        # Creating blank row in "results" table where the scores will be later stored
        detailsid = db.execute("SELECT id FROM surveydetails WHERE hash_id = ?", hashed_surveyid)[0]["id"]
        db.execute("INSERT INTO results (survey_id) VALUES (?)", detailsid)
        
        return render_template("surveycreated.jinja-html", hashed_surveyid=hashed_surveyid)
    else:
        return render_template("createsurvey.jinja-html")

@app.route("/insertsurveyid", methods=["GET", "POST"])
def insertsurveyid():
    if request.method == "POST":
        surveyid = request.form.get("surveyid")
        # Get list of surveysid to check if provided surveyid exists
        surveycheck = db.execute("SELECT * FROM surveysid WHERE hash_id = ?", surveyid)
        if len(surveycheck) == 0:
            message = "Please insert existing survey ID"
            return render_template("insertsurveyid.jinja-html", message=message)
        factor2 = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor2_name"]
        factor3 = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor3_name"]
        factors_list = ["Price", factor2, factor3]
        comb = makeList(surveyid)
        eight_list = [*range(8)]
        random = sample(eight_list,8)
       
        return render_template("surveyoverview.jinja-html", comb=comb, factors_list=factors_list, random=random, surveyid=surveyid)
    else:
        return render_template("insertsurveyid.jinja-html")
    
@app.route("/answersubmitted", methods=["GET","POST"])
def answersubmitted():
    if request.method == "POST":
       
        # Getting string looking like a list: "['["X", "X", ...]']"
        ranking = request.form.getlist("rankingarray")
        surveyid = request.form.get("surveyid")
        # Converting ranking to an actual list: ["X", "X", ...]
        ranking = ast.literal_eval(ranking[0])
        
        # Default ranking order has the format of list of integers: [1, 2, ...]
        # If list is not made of integers (is not default), then change it to be one
        if not all(isinstance(i, int) for i in ranking):
            ranking = [int(i[-1]) for i in ranking]
    
        # Now ranking is a list of elements in the order that the user chose, from the best to the worst
        # Value of each element represents specific combination, e.g.: 
        # Value "0" represents combination (UP, UF2, UF3)
        # Value "7" represents combination (CP, UF2, UF3)
        # For reference look in myfunctions.py
        
        # Each place gets its scores from 7 to 0 depending on a place
        # First place gets 7 points, second place gets 6, ... last place gets 0 point
        surveyid_nothashed = db.execute("SELECT id FROM surveydetails WHERE hash_id = ?", surveyid)[0]["id"]
        addscores(ranking, surveyid_nothashed)
        
        initialprices = db.execute("SELECT * FROM surveydetails WHERE id = ?", surveyid_nothashed)
        
        final_avg_price = calculateprice(initialprices, ranking)
        
            
        answercount = db.execute("SELECT * FROM results WHERE survey_id = ?", surveyid_nothashed)[0]["answercount"]
        if answercount == 1:
            db.execute("UPDATE results SET min_price = ?, avg_price = ?, max_price = ? WHERE survey_id = ?", final_avg_price, final_avg_price, final_avg_price, surveyid_nothashed)
        else:
            last_avg_price = db.execute("SELECT * FROM results WHERE survey_id = ?", surveyid_nothashed)[0]["avg_price"]
            new_avg_price = ((last_avg_price * (answercount - 1)) + final_avg_price) / answercount
            db.execute("UPDATE results SET avg_price = ? WHERE survey_id = ?", new_avg_price, surveyid_nothashed)
            
            last_min_price = db.execute("SELECT * FROM results WHERE survey_id = ?", surveyid_nothashed)[0]["min_price"]
            last_max_price = db.execute("SELECT * FROM results WHERE survey_id = ?", surveyid_nothashed)[0]["max_price"]
            if new_avg_price > last_max_price:
                db.execute("UPDATE results SET max_price = ? WHERE survey_id = ?", new_avg_price, surveyid_nothashed)
            elif new_avg_price < last_min_price:
                db.execute("UPDATE results SET min_price = ? WHERE survey_id = ?", new_avg_price, surveyid_nothashed)
                
        return redirect("/success")
    else:
        return redirect("/")

@app.route("/success", methods=["GET"])
def success():
    if request.referrer != "http://127.0.0.1:5000/insertsurveyid":
        return redirect("/")
    return render_template("thankyou.jinja-html")

@app.route("/mysurveys")
@login_required
def mysurveys():
    answercount = db.execute("SELECT * FROM results JOIN surveydetails ON results.survey_id = surveydetails.id JOIN surveysid ON surveydetails.survey_id = surveysid.id JOIN users on surveysid.user_id = users.id WHERE users.id = ?", session.get("user_id"))
    if len(answercount) != 0:
        surveydata = db.execute("SELECT * FROM results JOIN surveydetails ON results.survey_id = surveydetails.id JOIN surveysid ON surveydetails.survey_id = surveysid.id JOIN users on surveysid.user_id = users.id WHERE users.id = ?", session.get("user_id"))
        return render_template("mysurveys.jinja-html", surveydata=surveydata, nosurveys=0)
    else:
        return render_template("mysurveys.jinja-html", nosurveys=1)
    
@app.route("/details")
@login_required
def details():
    details = db.execute("SELECT * FROM surveydetails JOIN surveysid ON surveydetails.survey_id = surveysid.id JOIN users on surveysid.user_id = users.id WHERE users.id = ?", session.get("user_id"))
    if len(details) != 0:
        return render_template("details.jinja-html", details=details, nosurveys=0)
    else:
        return render_template("details.jinja-html", nosurveys=1)
