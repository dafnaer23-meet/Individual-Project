from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase



firebaseConfig = {
  "apiKey": "AIzaSyCfqGVJwOu3cfWRUOXFNlqbfO-bCpuCuM4",
  "authDomain": "project-72cd5.firebaseapp.com",
  "databaseURL": "https://project-72cd5-default-rtdb.firebaseio.com",
  "projectId": "project-72cd5",
  "storageBucket": "project-72cd5.appspot.com",
  "messagingSenderId": "789369560609",
  "appId": "1:789369560609:web:9e1f311cebcd65c2248d60",
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'



@app.route('/', methods=['GET', 'POST'])
def my_home():
  user = ""
  return render_template("home.html", user = user  )

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  error = " "
  if request.method == "POST":
    email=request.form['email']
    password=request.form['password']
    try:
      login_session["user"] = auth.sign_in_with_email_and_password(email, password)
      return redirect(url_for('add_post'))

    except:
      return "error"
  else:
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'GET':
    # dict_user=db.child("Users").child(login_session['user']['localId']).set(dict_user)
    # dict_user = {'email':'email','password':'password','full_name':'full_name','bio':'bio'}
    return render_template("signup.html")
  else:
    # email=request.form['email']
    # password=request.form['password']
    # username=request.form['username']
    # full_name=request.form['full_name']
    # bio=request.form["bio"]
    login_session['email'] = request.form['email']
    login_session['password'] = request.form['password']
    email = login_session['email']
    password = login_session['password'] 
    login_session['user'] = auth.create_user_with_email_and_password(email, password)
    user={"full_name":request.form["full_name"], "bio":request.form["bio"]}
    db.child("Users").child(login_session["user"]["localId"]).set(user)
    return redirect(url_for('signin'))

@app.route('/home', methods=['GET', 'POST'])
def home():
  user = db.child("Users").child(login_session['user']['localId']).get().val()
  return render_template("home.html", user = user)


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
  if request.method=="POST": 
    post={"username":request.form["username"], "picture":request.form["picture"]}
    db.child("posts").push("post")
    return redirect(url_for('the_post'))
  else:
    return render_template("add_post.html")

@app.route('/all_posts', methods=['GET', 'POST'])
def the_post():
  posts = db.child("post").get().val()

    @app.route('/signout')
def signout():
  login_session['user'] = None
auth.current_user = None
return redirect(url_for('signin'))


#create a new route called all_tweets and an html page called "tweets.html"
# display the tweets with the child "Tweets" and with .get().val()


if __name__ == '__main__':
    app.run(debug=True)