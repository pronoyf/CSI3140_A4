
Hospital Application that administers patients


For the development of our application, we used:

MySQL for the implementation of the database.
Apache Tomcat for client-server communication.
Python Flask for the server side of the application.
HTML and CSS and javascript for the client side of the application.
SQLAlchemy 

Prerequisites
MySQL
Xampp
An IDE of your choice (preferably Visual Studio)
Python Flask
HTML and CSS
A MySQL connector
Assuming you’re using Visual Studio, download extensions for:
jinja for client side
python flask
HTML
SQLAlchemy
Installation
Download the submitted project folder.

Install the following software:

MySQL
Xampp
An IDE of your choice (preferably Visual Studio)
Python Flask
HTML and CSS and javascript
A MySQL connector
SQLAlchemy

Using command interface run these installation commands:

pip install Flask SQLAlchemy pymysql Flask-Login Flask-Mail
pip install mysql-connector-python
pip install pymysql


Open the project folder using the IDE of your choice (Visual Studio).

Run your Xampp manager and start the following servers:

MySQL database server
Apache Web Server
Navigate to phpMyAdmin through your Xampp manager.

Create a new database and import the hospital_db.sql file submitted in the project folder. Now your database is set up.

Navigate back to your IDE and run the main.py file in the project folder. You should then get a hyperlink in the terminal that takes you to our website.






Patient Perspective
    Sign Up
    Navigate to the signup page
    Fill in your details including username, first name, last name, phone number, email, address, and password.
    Click "Signup".


    Navigate to the login page.
    Enter your username and password.
    Click "Login".
    Dashboard:

    After logging in, you will be redirected to the patient dashboard.
    The dashboard displays your name and allows you to submit a request to join the queue.
    Fill in the severity of your condition and submit the form to join the queue.
    The dashboard also displays the status of your queue requests as either "waiting" or "completed".

Staff Perspective
    Sign Up:

    Navigate to the signup page, then click the button that says staff signup
    Fill in your details including username, first name, last name, phone number, email, address, and password.
    Click "Signup".

    Login:

    Navigate to the login page then click the button that says staff login.
    Enter your username and password.
    Click "Login".

    Dashboard:

    After logging in, you will be redirected to the staff dashboard.
    The dashboard displays all queue requests with details including queue ID, patient ID, severity, wait time, and status.
    For each queue request with status "waiting", there is a button to admit the patient.
    Clicking the "Admit" button changes the queue status to "completed" and reduces the wait times of all other waiting patients by 5 minutes.

As a staff you are not allowed to access the patient dashboard and same is true for patient with the staff dashboard

login is required to access either dashboard and a logout is required to switch from patient to staff

