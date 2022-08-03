    try:
      login_session['user'] = auth.sign_in_with_email_and_password(login_session['email'], login_session['password'])
      return redirect(url_for('add_tweet'))
    except:
      error = "Authentication failed"
      return error
      #64, between signup to
      @app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
  # create a dictionary called 'tweet' that has 3 key: 
  # title and text, the values are the inputs from the form
  tweet={"title":request.form["title"], "text":request.form["text"], "uid":login_session["user"]["localId"]}
  # uid: the value is the localId from the login_session
  # add "Tweets" child to database and push the new tweet (the new dictionary)
  db.child("tweets").push("tweet")
####### all of this can be found in the slides ###########
  return render_template("add_tweet.html")

  @app.route('/all_tweets', methods=['GET', 'POST'])
def the_tweet():
  tweets = db.child("tweet").get().val()