#!/usr/bin/python3
# written by andrewt@cse.unsw.edu.au October 2017
# as a starting point for COMP[29]041 assignment 2
# https://cgi.cse.unsw.edu.au/~cs2041/assignments/UNSWtalk/


# No info passed, initialise to "" or N/A
##################################################################

import os
from flask import Flask, render_template, session, request,redirect
import re
from datetime import datetime
import random

students_dir = "dataset-small";
masUsername = ""
masPassword = ""
masFullName = ""
masSuburb = ""
masEmail = ""
masUni = ""
masDob = ""
masProgram = ""
masZid = ""
masAddress = []
masFriends = []
masCourses = []

app = Flask(__name__)

def matchLogin(string,pattern):
    match = re.search(pattern,string)
    realMatch = match.group(1) if match else ""
    return realMatch

def getPosts(user):
    posts = []
    students = sorted(os.listdir(students_dir))
    student_to_show = user
    for filename in os.listdir(os.path.join(students_dir,student_to_show)):
        if(re.match(r'\d',filename)):
            fileDetails = os.path.join(students_dir,student_to_show,filename)
            with open(fileDetails) as f:
                details = f.read()

                posts.append(details)
    return posts
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
            realPassword = matchLogin(details,'password: *(.*)')
            realName = matchLogin(details,'full_name: *(.*)')
            realFriends = matchLogin(details,'friends: *\((.*)\)')
            realCourses = matchLogin(details,'courses: *\((.*)\)')
            realProgram = matchLogin(details,'program: *(.*)')
            realEmail = matchLogin(details,'email: *(.*)')
            realZid = matchLogin(details,'zid: *(.*)')
            realBirthday = matchLogin(details,'birthday: *(.*)')
            realSuburb = matchLogin(details,'home_surburb: *(.*)')
            realLat = matchLogin(details,'home_latitude: *(.*)')
            realLng = matchLogin(details,'home_longitude: *(.*)')
            if realPassword == password:
                session['username'] = username
                session['password'] = password
                session['name'] = realName
                session['program'] = realProgram
                session['email'] = realEmail
                session['zid'] = realZid
                session['suburb'] = realSuburb
                session['birthday'] = realBirthday
                masFriends = realFriends.split(',')
                for x in masFriends:
                    x = re.sub(r'^ +',"",x)
                masCourses = realCourses.split(',')
                session['friends'] = masFriends
                session['course'] = masCourses
                masAddress.append(realLat)
                masAddress.append(realLng)
                session['address'] = masAddress
                masPosts = getPosts(username)
                img = "/static/"+students_dir+"/"+username+"/img.jpg"
                # if no image pass question mark image
                session['img'] = img
                post = None
                return redirect("/profilePage", code=302)
                #return render_template('profilePage.html',user=username,name=realName,
                 #prog=realProgram, email=realEmail, zid=realZid,sub=realSuburb,
                 #dob=realBirthday,courses=masCourses,posts=masPosts,img = img)
            else:
                error= "Invalid Username or Password choice. Please enter a vlid Username and Password"
                return render_template('login.html',error=error)
    error= "Invalid Username or Password choice. Please enter a valid Username and Password333"
    return render_template('login.html',error=error)

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

@app.route('/feed',methods=['GET','POST'])
def feed():
    masUsername = session['username']
    img = session['img']
    masFriends = session['friends']
    feedPosts = getPosts(masUsername)
    for x in masFriends:
        if len(feedPosts) > 50:
            break
        feedPosts.extend(getPosts(x.strip()))
    random.shuffle(feedPosts)
    return render_template('feed.html', user=masUsername, img=img,
    posts = feedPosts)


@app.route('/profilePage',methods=['GET','POST'])
def profilePage():
    maxi = None
    temp = None
    masUsername = session['username']
    newPost = request.form.get('post')
    if newPost:
        newPost = "message: " + newPost
        # Following 2 lines are from
        # https://stackoverflow.com/questions/10624937/convert-datetime-object-to-a-string-of-date-only-in-python#10
        now=datetime.now()
        newPost = newPost+"\nTime:"+now.isoformat()
        newPost = newPost + "\nFrom:"+masUsername
        maxi = 1
        for filename in os.listdir(os.path.join(students_dir,masUsername)):
            temp = re.search(r'^(\d).',filename)
            match = temp.group(1) if temp else ""
            if temp:
                if match > maxi:
                    maxi = match
        maxi = int(maxi)
        maxi = maxi + 1
        maxi = str(maxi)
        maxi = maxi+".txt"
        file = open(os.path.join(students_dir,masUsername,maxi), 'w')
        file.write(newPost)
        file.close()
    masPassword = session['password']
    masFullName = session['name']
    masProgram = session['program']
    masEmail = session['email']
    masZid = session['zid']
    masSuburb = session['suburb']
    masDob = session['birthday']
    masCourses = session['course']
    masPosts = getPosts(masUsername)
    img = session['img']
    return render_template('profilePage.html',user=masUsername,name=masFullName,
     prog=masProgram, email=masEmail, zid = masZid,sub= masSuburb,
     dob = masDob,courses=masCourses,posts=masPosts, img=img, newPost=newPost,maxi=maxi)

@app.route('/friendList',methods=['GET','POST'])
def friendsList():
    masUsername = session['username']
    masFriends = session['friends']
    img = session['img']
    return render_template('friendList.html',user=masUsername, friends=masFriends,img=img)

@app.route('/<friend>',methods=['GET','POST'])
def displayFriendPage(friend):
    masUsername = session['username']
    masPosts = getPosts(masUsername)
    students = sorted(os.listdir(students_dir))
    details_filename = os.path.join(students_dir,friend, "student.txt")
    with open(details_filename) as f:
        details = f.read()
    realName = matchLogin(details,'full_name: *(.*)')
    realFriends = matchLogin(details,'friends: *\((.*)\)')
    realCourses = matchLogin(details,'courses: *\((.*)\)')
    realProgram = matchLogin(details,'program: *(.*)')
    realEmail = matchLogin(details,'email: *(.*)')
    realZid = matchLogin(details,'zid: *(.*)')
    realBirthday = matchLogin(details,'birthday: *(.*)')
    realSuburb = matchLogin(details,'home_surburb: *(.*)')
    realPosts = getPosts(friend)
    img = session['img']
    return render_template('showFriend.html',user=masUsername,name=realName,
    prog=realProgram, email=realEmail, zid = realZid,sub= realSuburb,
    dob = realBirthday,courses=realCourses,friends=realFriends,friend=friend
    ,img=img,posts=realPosts)

@app.route('/settings',methods=['GET','POST'])
def showSettings():
    masUsername = session['username']
    img = session['img']
    return render_template('settings.html', user=masUsername, img=img)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)



#<form method="POST" action="homePage">
#<li><input type="submit" value="Logout" class="unswtalk_button"></li>
#</form>
