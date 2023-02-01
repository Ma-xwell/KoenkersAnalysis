# Simple conjoint analysis
#### Video Demo:  <URL HERE>
#### Description:

## **Main purpose**
This web application is designed for the purpose of determining the most competitive price for the product.

Let's say the user wants to launch a new product and doesn't know what price would be the best (the most attractive to the customers). In order to know that, they can compare their new potential product with the one already existing on the market (for example the competition's product).

The application allows user to create their own survey with 2 products with 3 factors each (first one is the price, the second and the third ones are named by the user). User can share the survey to external participants. All the possible combinations (eight) are presented to the surveyed people, which have to sort the combinations in order from top to bottom (from the best to the worst in their opinion). It is worth to mention that all the possibilities are shown randomly each time, so no unconscious imposition is being made towards the surveyed people.

Program continuously calculates the most competitive price based on the incoming answers.

Also, the user can easily see the overview and details of each survey they created by clicking on the specific options in menu.

## **Technologies used:**
- HTML
- CSS
- Bootstrap
- JavaScript
- jQuery
- jQuery UI
- Python
- Flask
- Jinja
- SQLite

## **Description of each file**

### **HTML - Jinja**
- **changepassword.jinja-html:** 
    - Allows logged user to change their password.
- **createsurvey.jinja-html:** 
    - Allows logged user to create survey. Logged user provides names of factor no. 2 and factor no. 3. The factor no. 1 is determined upfront as "Price". Logged user also provides potential price for their product, value of factor no. 2, factor no. 3 and does the same with the competition's product.
- **details.jinja-html:** 
    - Shows the details of each survey the logged user ever created (survey ID, their option, competition's option).
- **index.jinja-html:**
    - Homepage; consists of overall description and instruction for using the website.
- **insertsurveyid.jinja-html:**
    - Page where logged user or any other external user can insert survey ID and click "Submit" in order to be redirected to the page **surveyoverview.jinja-html**.
- **layout.jinja-html:**
    - Simple layout which differentiates between logged and not logged users, showing them specific options on the top navigation bar.
- **login.jinja-html:**
    - Allows registered user to Log In to their account.
- **mysurveys.jinja-html:**
    - Shows the table with logged user's surveys' IDs, number of submissions, calculated average prices (the most competitive ones) along with the minimal and maximal average prices ever calculated. Each row represents other survey created by the logged user.
- **register.jinja-html:**
    - Allows anyone to register to the system and gain fully functional account.
- **surveycreated.jinja-html:**
    - Page where the logged user is redirected to when they successfully create the survey.4
- **surveyoverview.jinja-html:**
    - The page which **insertsurveyid.jinja-html:** redirects to. It consists of sortable elements, which determine how good the specific option appears to the surveyed person. The surveyed person sorts the items from the best to the worst in their opinion, from top to bottom. From the option they would be most likely to buy, to the one they would be least likely to buy.
- **thankyou.jinja-html:**
    - After the survey is submitted, this is the page where the surveyed person is redirected to. This page can only be accessed by redirection from successful submission of the survey.

### **Python**
- **app.py:**
    - Main application's file, where all the redirections happen. Also it connects to the database and provides with all the needed variables calculated on the server side and performs changes in said database.
- **myfunctions.py:**
    - Helper file which consists of functions which allow to perform more complex calculations and operations on the database.

### **JavaScript - jQuery UI**
- **dragscript.js:**
    - jQuery UI script which allows the items in **surveyoverview.jinja-html** to be sortable. It also tracks their current position and sends it back to **surveyoverview.jinja-html** which then sends it back to the server side - **app.py**.
- **script.js:**
    - Script connected with **createsurvey.jinja-html**. It takes the responsibilty of the proper responsiveness and also collects the data and sends it back to the jinja-html web, which then sends them back to the server side - **app.py**.

### **CSS**
- **styles.css:**
    - This file is responsible for extremely basic styling as the main part of styling is done via Bootstrap (using classes)

### **SQLite**
- **database.db:**
    - Database consisting of tables:
        - *users*: storing logins and passwords of the users.
        - *surveysid*: storing survey IDs (it is worth to mention that IDs are all hashed, so external users will not be able to substract or add any number to ID known by them and access random survey they should not have access to) and user_id as a foreign key to *users* table.
        - *surveydetails*: storing names and values of all the factors along with the survey ID (not hashed) as a foreign key to *surveysid* table.
        - *results*: storing sum of all the scores which were calculated for each combination (option) shown to the surveyed people. It is also storing number of submissions, average price, minimal and maximal average price ever calculated for the survey. Survey ID (not hashed) is a foreign key to *surveydetails* table.
