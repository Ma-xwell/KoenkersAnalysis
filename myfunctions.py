# File containing functions without decorators

from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL

# Connecting database (SQLite3)
db = SQL("sqlite:///database.db")

# Function copied from CS50 Finance Project
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def makeList(surveyid):
    # List of all (8) possible combinations
    comb = [[0, 0, 0] for i in range(8)]

    # U - user
    # C - competition
    # P - price
    # F2 - factor 2
    # F3 - factor 3
    
    # First combination (UP, UF2, UF3)
    comb[0][0] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["priceyou"]
    comb[0][1] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor2_youvalue"]
    comb[0][2] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor3_youvalue"]
    # Second combination (UP, UF2, CF3)
    comb[1][0] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["priceyou"]
    comb[1][1] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor2_youvalue"]
    comb[1][2] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor3_compvalue"]
    # Third combination (UP, CF2, UF3)
    comb[2][0] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["priceyou"]
    comb[2][1] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor2_compvalue"]
    comb[2][2] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor3_youvalue"]
    # Fourth combination (UP, CF2, CF3)
    comb[3][0] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["priceyou"]
    comb[3][1] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor2_compvalue"]
    comb[3][2] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor3_compvalue"]
    # Fifth combination (CP, CF2, CF3)
    comb[4][0] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["pricecomp"]
    comb[4][1] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor2_compvalue"]
    comb[4][2] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor3_compvalue"]
    # Sixth combination (CP, CF2, UF3)
    comb[5][0] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["pricecomp"]
    comb[5][1] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor2_compvalue"]
    comb[5][2] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor3_youvalue"]
    # Seventh combination (CP, UF2, CF3)
    comb[6][0] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["pricecomp"]
    comb[6][1] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor2_youvalue"]
    comb[6][2] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor3_compvalue"]
    # Eighth combination (CP, UF2, UF3)
    comb[7][0] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["pricecomp"]
    comb[7][1] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor2_youvalue"]
    comb[7][2] = db.execute("SELECT * FROM surveydetails WHERE hash_id = ?", surveyid)[0]["factor3_youvalue"]
    
    return comb

# Updating the results tab
def addscores(ranking, surveyid_nothashed):
    for i in ranking:
        score = 7 - i
        if ranking[i] == 0:
            db.execute("UPDATE results SET comb0 = comb0 + ? WHERE survey_id = ?", score, surveyid_nothashed)
        elif ranking[i] == 1:
            db.execute("UPDATE results SET comb1 = comb1 + ? WHERE survey_id = ?", score, surveyid_nothashed)
        elif ranking[i] == 2:
            db.execute("UPDATE results SET comb2 = comb2 + ? WHERE survey_id = ?", score, surveyid_nothashed)
        elif ranking[i] == 3:
            db.execute("UPDATE results SET comb3 = comb3 + ? WHERE survey_id = ?", score, surveyid_nothashed)
        elif ranking[i] == 4:
            db.execute("UPDATE results SET comb4 = comb4 + ? WHERE survey_id = ?", score, surveyid_nothashed)
        elif ranking[i] == 5:
            db.execute("UPDATE results SET comb5 = comb5 + ? WHERE survey_id = ?", score, surveyid_nothashed)
        elif ranking[i] == 6:
            db.execute("UPDATE results SET comb6 = comb6 + ? WHERE survey_id = ?", score, surveyid_nothashed)
        elif ranking[i] == 7:
            db.execute("UPDATE results SET comb7 = comb7 + ? WHERE survey_id = ?", score, surveyid_nothashed)
            
    db.execute("UPDATE results SET answercount = answercount + 1 WHERE survey_id = ?", surveyid_nothashed)
       
# Function calculates competitive price for user's product basing on prices and scores
def calculateprice(initialprices, ranking):
    ranking_scores = [0]*8
    for i in ranking:
        score = 7 - i
        if ranking[i] == 0:
            ranking_scores[0] = ranking_scores[0] + score
        elif ranking[i] == 1:
            ranking_scores[1] = ranking_scores[1] + score
        elif ranking[i] == 2:
            ranking_scores[2] = ranking_scores[2] + score
        elif ranking[i] == 3:
            ranking_scores[3] = ranking_scores[3] + score
        elif ranking[i] == 4:
            ranking_scores[4] = ranking_scores[4] + score
        elif ranking[i] == 5:
            ranking_scores[5] = ranking_scores[5] + score
        elif ranking[i] == 6:
            ranking_scores[6] = ranking_scores[6] + score
        elif ranking[i] == 7:
            ranking_scores[7] = ranking_scores[7] + score
            
    # FACTOR 1 - price
    # Calculating scores for user's factor 1; combinations: 0, 1, 2, 3
    userscore_factor1 = (ranking_scores[0] + ranking_scores[1] + ranking_scores[2] + ranking_scores[3]) / 4
    # Calculating scores for competition's factor 1; combinations: 4, 5, 6, 7
    compscore_factor1 = (ranking_scores[4] + ranking_scores[5] + ranking_scores[6] + ranking_scores[7]) / 4
    
    # FACTOR 2
    # Calculating scores for user's factor 2; combinations: 0, 1, 6, 7
    userscore_factor2 = (ranking_scores[0] + ranking_scores[1] + ranking_scores[6] + ranking_scores[7]) / 4
    # Calculating scores for competition's factor 2; combinations: 2, 3, 4, 5
    compscore_factor2 = (ranking_scores[2] + ranking_scores[3] + ranking_scores[4] + ranking_scores[5]) / 4
    
    # FACTOR 3
    # Calculating scores for user's factor 3; combinations: 0, 2, 5, 7
    userscore_factor3 = (ranking_scores[0] + ranking_scores[2] + ranking_scores[5] + ranking_scores[7]) / 4
    # Calculating scores for competition's factor 3; combinations: 1, 3, 4, 6
    compscore_factor3 = (ranking_scores[1] + ranking_scores[3] + ranking_scores[4] + ranking_scores[6]) / 4
    
    # Calculate difference between user's scores and competition's scores in factor 1
    difference_f1 = userscore_factor1 - compscore_factor1
    if difference_f1 == 0:
        maxprice = userscore_factor1
        return maxprice
    print("difference_f1: " + str(difference_f1))
    # Calculate difference between user's scores and competition's scores in factor 2
    difference_f2 = userscore_factor2 - compscore_factor2
    print("difference_f2: " + str(difference_f2))
    # Calculate difference between user's scores and competition's scores in factor 3
    difference_f3 = userscore_factor3 - compscore_factor3
    print("difference_f3: " + str(difference_f3))
    
    # Calculating difference between proposed prices
    price_user = initialprices[0]["priceyou"]
    price_comp = initialprices[0]["pricecomp"]
    difference_price = price_user - price_comp
    print("difference_price: " + str(difference_price))
    # Calculating the value of one utility unit
    util_value = difference_price / difference_f1
    print("util_value: " + str(util_value))
    # Check balance in scores - who has more scores in total
    scores_balance = difference_f1 + difference_f2 + difference_f3
    print("scores_balance: " + str(scores_balance))
    print(ranking)
    print(ranking_scores)
    # Final maximal competitive price
    max_price = price_comp + (util_value * scores_balance)
    print(util_value * scores_balance)
    print(max_price)
    
    return max_price
