#!/usr/bin/python3
# written by andrewt@cse.unsw.edu.au October 2017
# as a starting point for COMP[29]041 assignment 2
# https://cgi.cse.unsw.edu.au/~cs2041/assignments/UNSWtalk/

import os
from flask import Flask, render_template, session, request
import re

students_dir = "dataset-small";
masUsername = ""
masPassword = ""
fullName = ""
suburb = ""
email = ""
uni = ""
dob = ""
address = []
friends = []
courses = []

app = Flask(__name__)

#Show unformatted details for student "n".
# Increment  n and store it in the session cookie

@app.route('/', methods=['GET','POST'])
@app.route('/homePage', methods=['GET','POST'])
def begin():
    return render_template('homePage.html')

@app.route('/mainPage', methods=['GET','POST'])
def start():
    n = session.get('n', 0)
    students = sorted(os.listdir(students_dir))
    student_to_show = students[n % 3]
    details_filename = os.path.join(students_dir,student_to_show, "student.txt")
    with open(details_filename) as f:
        details = f.read()
    session['n'] = n + 1
    return render_template('mainPage.html')

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    return render_template('login.html',error = error)

@app.route('/register', methods=['GET','POST'])
def register():
    error = None
    return render_template('register.html',error = error)

@app.route('/authenLog',methods=['GET','POST'])
def authenLog():
    username = request.form.get('username','')
    #get Username from input
    #fix up input conditions for security
    password = request.form.get('password','')
    if len(username) > 32:
        username = username[:32]
    username = re.sub(r'\@|\||\<|\>|\#',"",username)
    if len(password) > 32:
        password = password[:32]
    if username == "" or password == "" or len(username) < 8 or len(password) < 1:
        error = "Invalid Username or Password choice. Please choose a valid Username or Password1111"
        return render_template('login.html',error=error)
    password = re.sub(r'\@|\||\<|\>|\#',"",password)
    students = sorted(os.listdir(students_dir))
    for x in students:
        if re.match(r''+username+'',x):
            details_filename = os.path.join(students_dir,username, "student.txt")
            with open(details_filename) as f:
                details = f.read()
            match = re.search('password: *(.*)',details)
            realPassword = match.group(1) if match else ""
            if realPassword == password:
                match = research('friends:\((.*)\)',details)

                match = research('',details)
                match = research('',details)
                match = research('',details)
                match = research('',details)
                match = research('',details)
                match = research('',details)
                masUsername = username
                masPassword = password
                return render_template('mainPage.html')
            else:
                error= "Invalid Username or Password choice. real password is(" + realPassword
                return render_template('login.html',error=error)
    error= "Invalid Username or Password choice. Please enter a valid Username and Password333"
    return render_template('login.html',error=error)
    #check for username and password in dataset then authenticate login
    #if not re.match(r'\@',email):
    #    error = "Invalid Email. Please enter a valid Email"
    #    return render_template('register.html',error=error)

@app.route('/authenRegi',methods=['GET','POST'])
def authenRegi():
    username = request.form.get('username','')
    #get Username from input
    #fix up input conditions for security
    password = request.form.get('password','')
    if len(username) > 32:
        username = username[:32]
    username = re.sub(r'\@|\||\<|\>|\#',"",username)
    if len(password) > 32:
        password = password[:32]
    if username == "" or password == "" or len(username) < 8 or len(password) < 8:
        error = "Invalid Username or Password choice. Please choose a valid Username or Password"
        return render_template('register.html',error=error)
    password = re.sub(r'\@|\||\<|\>|\#',"",password)
    email = request.form.get('email','')
    email = request.form.get('email','')
    if not re.match(r'\@',email):
        error = "Invalid Email. Please enter a valid Email"
        return render_template('register.html',error=error)
    return render_template('mainPage.html',username=username,password=password)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)

def displayFriends():
    n = session.get('n', 0)
    students = sorted(os.listdir(students_dir))
    student_to_show = students[n % 3]
    details_filename = os.path.join(students_dir,student_to_show, "student.txt")
    with open(details_filename) as f:
        details = f.read()
    session['n'] = n + 1
    return render_template('feed.html',student_details=details)
