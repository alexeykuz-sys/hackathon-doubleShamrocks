import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm,\
    ChangeUsernameForm, ChangePasswordForm
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from bson.objectid import ObjectId
import cloudinary
import cloudinary.uploader
import cloudinary.api
from datetime import date
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)

mongo = PyMongo(app)


@app.route("/")
@app.route("/homepage", methods=["GET", "POST"])
def homepage():
    return render_template("home.html")


@app.route("/jokes", methods=["GET", "POST"])
def jokes():
    jokes = list(mongo.db.jokes.find())
    return render_template("jokes.html", jokes=jokes)


@app.route('/joke_like/<joke_id>', methods=["GET", "POST"])
def joke_like(joke_id):
    joke = mongo.db.jokes.update_one(
        {"_id": ObjectId(joke_id)},
        {'$inc': {'likes': 1}},
        upsert=True
        )
    jokes = list(mongo.db.jokes.find())
    return render_template("jokes.html", jokes=jokes)


@app.route('/joke_dislike/<joke_id>', methods=["GET", "POST"])
def joke_dislike(joke_id):
    joke = mongo.db.jokes.update_one(
        {"_id": ObjectId(joke_id)},
        {'$inc': {'dislikes': 1}},
        upsert=True
    )
    jokes = list(mongo.db.jokes.find())
    return render_template("jokes.html", jokes=jokes)


@app.route("/videos", methods=["GET", "POST"])
def videos():
    videos = list(mongo.db.videos.find())
    return render_template("videos.html", videos=videos)


@app.route('/video_like/<video_id>', methods=["GET", "POST"])
def video_like(video_id):
    video = mongo.db.videos.update_one(
        {"_id": ObjectId(video_id)},
        {'$inc': {'likes': 1}},
        upsert=True
        )
    videos = list(mongo.db.videos.find())
    return render_template("videos.html", videos=videos)


@app.route('/video_dislike/<video_id>', methods=["GET", "POST"])
def video_dislike(video_id):
    video = mongo.db.videos.update_one(
        {"_id": ObjectId(video_id)},
        {'$inc': {'dislikes': 1}},
        upsert=True
    )
    videos = list(mongo.db.videos.find())
    return render_template("videos.html", videos=videos)


# ADD VIDEO
@app.route("/profile/<username>/upload_video", methods=["GET", "POST"])
def upload_video(username):

    user_id = mongo.db.users.find_one({'username': session['username']})['_id']
    user = mongo.db.users.find_one(
          {"username": session['username']})['username']
    # returns a list of videos asigned to that user
    my_video = list(mongo.db.videos.find({'user': user_id}))

    if request.method == 'POST':
        # gets data from form to upload
        for user_video in request.files.getlist("user_videos"):

            filename = secure_filename(user_video.filename)
            filename, file_extension = os.path.splitext(filename)
            public_id_video = ("vidoes/" + username + "/" + filename)
            
            # uploads video to cloudinary
            cloudinary.uploader.unsigned_upload(
                user_video, "puppy_image",
                cloud_name='puppyplaymates',
                folder='/doubleshamrocks/', public_id=public_id_video,
                resource_type="video")

            # creates a url for the database
            video_url = (
                "https://res.cloudinary.com/puppyplaymates/video/upload/doubleshamrocks/"
                + public_id_video + file_extension)

            # adds video parameters
            today = date.today()
            new_video = {
                "user": user_id,
                "video_url": video_url,
                "video_title": request.form.get('video_title'),
                "video_description": request.form.get('video_description'),
                "author": username,
                "date": today.strftime("%d/%m/%Y"),
                'likes': 0,
                'dislikes': 0
            }

            # uploads to database
            mongo.db.videos.insert_one(new_video)

            # Adds a video_id to the users video array
            video_id = mongo.db.videos.find_one(
                {'video_url': video_url})['_id']

            mongo.db.users.update_one(
                {"username": username},
                {"$addToSet": {"video": video_id}})

        return redirect(url_for('upload_video', username=username))
    return render_template(
        "upload_video.html", user=user, username=username, my_video=my_video)


# ADD JOKES
@app.route("/profile/<username>/upload_jokes", methods=["GET", "POST"])
def upload_jokes(username):

    user_id = mongo.db.users.find_one({'username': session['username']})['_id']
    user = mongo.db.users.find_one(
        {"username": session['username']})['username']
    # returns a list of jokes asigned to that user
    my_jokes = list(mongo.db.jokes.find({'user': user_id}))

    if request.method == 'POST':
        # gets data from form to upload and creates joke object
        today = date.today()
        new_joke = {
            "user": user_id,
            "joke": request.form.get('user_jokes'),
            "date": today.strftime("%d/%m/%Y"),
            "author": username,
            'likes': 0,
            'dislikes': 0,
        }

        # adds joke to both databases parameters
        mongo.db.jokes.insert_one(new_joke)

        # gets the new object id thats been created to pass into users
        joke_id = mongo.db.jokes.find_one(
            {'joke': request.form.get('user_jokes')})['_id']

        mongo.db.users.update_one(
            {"username": username},
            {"$addToSet": {"joke": joke_id}})

        return redirect(url_for('upload_jokes', username=username))
    return render_template(
        "upload_jokes.html", user=user, username=username, my_jokes=my_jokes)


@app.route("/upload_image", methods=["GET", "POST"])
def upload_image():

    username = "testing"
    user = mongo.db.users.find_one({"username": username})

    if request.method == 'POST':
        for item in request.files.getlist("user_image"):
            filename = secure_filename(item.filename)
            filename, file_extension = os.path.splitext(filename)
            public_id_image = (username + '/' + filename)
            cloudinary.uploader.unsigned_upload(
                item, "puppy_image", cloud_name='puppyplaymates',
                folder='/doubleshamrocks/', public_id=public_id_image)
            image_url = (
                "https://res.cloudinary.com/puppyplaymates/image/upload/doubleshamrocks/"
                + public_id_image + file_extension)

            mongo.db.users.update(
                {"username": username},
                {"$addToSet": {"user_image": {
                    "image_url": image_url,
                    "image_title": request.form.get('image_title'),
                    "image_description": request.form.get('image_description')
                }}})

        return redirect(url_for('upload_image'))
    return render_template("upload_image.html", user=user)


@app.route('/edit_joke/<joke_id>')
def edit_joke(joke_id):

    # prevents guest users from viewing the form
    if 'username' not in session:
        flash('You must be logged in to edit a joke!')
        return redirect(url_for('homepage'))
    user_in_session = mongo.db.users.find_one({'username': session['username']})
    # find the selected joke in DB by its id
    selected_joke = mongo.db.jokes.find_one({"_id": ObjectId(joke_id)})

    # allows only author of the joke to edit it;
    # protects againts brute-forcing
    if selected_joke['user'] == user_in_session['_id']:
        return render_template('edit_joke.html',
                               selected_joke=selected_joke)
    else:
        flash("You can only edit your own jokes!")
        return redirect(url_for('homepage'))


# Updatejoke in the Database
@app.route("/update_joke/<joke_id>", methods=["POST"])
def update_joke(joke_id):
    '''
    UPDATE.
    Updates the selected joke in the database after submission the form.
    '''
    selected_joke = mongo.db.jokes.find_one({"_id": ObjectId(joke_id)})
    # identifies the user in session to assign an author for edited joke
    username = session['username']
    user_id = mongo.db.users.find_one({'username': session['username']})['_id']
    likes = selected_joke['likes']
    dislikes = selected_joke['dislikes']

    if request.method == "POST":
        today = date.today()
        # updates the selected joke with data from the form
        mongo.db.jokes.update({"_id": ObjectId(joke_id)}, {
            "joke": request.form.get("joke"),
            "user": user_id,
            "date": today.strftime("%d/%m/%Y"),
            "author": username,
            "likes": likes,
            "dislikes": dislikes
        })
        return redirect(url_for("profile", username=session["username"]))


# Delete Joke
@app.route("/delete_joke/<joke_id>")
def delete_joke(joke_id):
    '''
    DELETE.
    Removes a joke from the database.
    Only the author of the joke can delete the joke.
    '''
    # prevents guest users from viewing the modal
    if 'username' not in session:
        flash('You must be logged in to delete a joke!')
        return redirect(url_for('homepage'))
    user_in_session = mongo.db.users.find_one(
        {'username': session['username']})
    # get the selected joke for filling the fields
    selected_joke = mongo.db.jokes.find_one({"_id": ObjectId(joke_id)})
    # allows only author of the joke to delete it;
    # protects againts brute-forcing
    if selected_joke['user'] == user_in_session['_id']:
        mongo.db.jokes.remove({"_id": ObjectId(joke_id)})
        # find the author of the  joke
        author = mongo.db.users.find_one(
            {'username': session['username']})['_id']

        mongo.db.users.update_one({"_id": ObjectId(author)},
                                  {"$pull": {"user_jokes": ObjectId(joke_id)}})
        flash('Your joke has been deleted.')
        return redirect(url_for("homepage"))
    else:
        flash("You can only delete your own jokes!")
        return redirect(url_for('homepage'))


@app.route("/login",  methods=['GET', 'POST'])
def login():
    '''
    The login function calls LoginForm class from the forms.py file,
    It checks if the inputed username and passwords are valid
    and then it adds a user to session.
    '''
    # Check if the user is already logged in
    if 'username' in session:
        flash('You are already logged in!')
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        users = mongo.db.users
        registered_user = users.find_one({'username':
                                          request.form['username']})

        if registered_user:
            # Check if password in the form is same as the password in the DB
            if check_password_hash(registered_user['password'],
                                   request.form['password']):
                # Add user to session if passwords match,
                # redirect user to the homepage after successfull login
                session['username'] = request.form['username']
                flash('You have been successfully logged in!')
                return redirect(url_for('homepage'))
            else:
                # if user entered incorrect password
                flash("Incorrect username or password. Please try again")
                return redirect(url_for('login'))
        else:
            # if user entered incorrect username
            flash("Username does not exist! Please try again")
            return redirect(url_for('login'))
    return render_template('login.html',  form=form)


# Register
@app.route("/register", methods=['GET', 'POST'])
def register():
    '''
    CREATE.
    Creates a new account for a new user; it calls the RegisterForm class
     from forms.py file.
    Checks if the username is not already excist in database,
    hashes the entered password and add a new user to session.
    '''
    # checks if user is not already has an account
    if 'username' in session:
        flash('You are already registered!')
        return redirect(url_for('homepage'))

    form = RegisterForm()
    if form.validate_on_submit():
        users = mongo.db.users
        # checks if the username is unique
        registered_user = mongo.db.users.find_one({'username':
                                                   request.form['username']})
        if registered_user:
            flash("Sorry, this username is already taken!")
            return redirect(url_for('register'))
        else:
            # hashes the entered password using werkzeug
            hashed_password = generate_password_hash(request.form['password'])
            new_user = {
                "username": request.form['username'],
                "password": hashed_password,
                "jokes": [],
                "videos": [],
                "images": [],
                "profile_image": "",
            }
            users.insert_one(new_user)
            # add new user to the session
            session["username"] = request.form['username']
            flash('Your account has been successfully created.')
            return redirect(url_for('homepage'))
    return render_template('register.html', form=form)


# Logout
@app.route("/logout")
def logout():
    '''
    Logs user out and redirects to home
    '''
    session.pop("username",  None)
    return redirect(url_for("homepage"))


# Profile
@app.route("/profile/<username>")
def profile(username):
    '''
    Profile page.
    '''
    # prevents guest users from viewing the page
    if 'username' not in session:
        flash('You must be logged in to view that page!')
    username = mongo.db.users.find_one({'username':
                                        session['username']})['username']
    image = mongo.db.users.find_one({'username':
                                     session['username']})['profile_image']
    user_id = mongo.db.users.find_one({'username': session['username']})['_id']
    my_jokes = mongo.db.jokes.find({'user': user_id})
    return render_template('profile.html',
                           image=image,
                           username=username,
                           my_jokes=my_jokes)


# Change username
@app.route("/change_username/<username>", methods=['GET', 'POST'])
def change_username(username):
    '''
    UPDATE.
    Allows user to change the current username.
    It calls the ChangeUsernameForm class from forms.py.
    Checks if the new username is unique and not exist in database,
    then clear the session and redirect user to login page.
    '''
    # prevents guest users from viewing the form
    if 'username' not in session:
        flash('You must be logged in to change username!')
    users = mongo.db.users
    form = ChangeUsernameForm()
    if form.validate_on_submit():
        # checks if the new username is unique
        registered_user = users.find_one({'username':
                                          request.form['new_username']})
        if registered_user:
            flash('Sorry, username is already taken. Try another one')
            return redirect(url_for('change_username',
                                    username=session["username"]))
        else:
            users.update_one(
                {"username": username},
                {"$set": {"username": request.form["new_username"]}})
        # clear the session and redirect to login page
        flash("Your username was updated successfully.\
                    Please, login with your new username")
        session.pop("username",  None)
        return redirect(url_for("login"))

    return render_template('change_username.html',
                           username=session["username"],
                           form=form)


# Delete Account
@app.route("/delete_account/<username>", methods=['GET', 'POST'])
def delete_account(username):
    '''
    DELETE.
    Remove user's account from the database as well as all
    uploaded jokes/videos created by this user.
    Before deletion of the account, user is asked
    to confirm it by entering password.
    '''
    # prevents guest users from viewing the form
    if 'username' not in session:
        flash('You must be logged in to delete an account!')
    user = mongo.db.users.find_one({"username": username})
    # checks if password matches existing password in database
    if check_password_hash(user["password"],
                           request.form.get("confirm_password_to_delete")):

        user_jokes = user.get("jokes")
        for joke in user_jokes:
            mongo.db.jokes.remove({"_id": joke})
        user_videos = user.get("videos")
        for video in user_videos:
            mongo.db.videos.remove({"_id": video})
        # remove user from database,clear session and redirect to the home page
        flash("Your account has been deleted.")
        session.pop("username", None)
        mongo.db.users.remove({"_id": user.get("_id")})
        return redirect(url_for("homepage"))
    else:
        flash("Password is incorrect! Please try again")
        return redirect(url_for("profile", username=username))


# Change password
@app.route("/change_password/<username>", methods=['GET', 'POST'])
def change_password(username):
    '''
    UPDATE.
    Allows user to change the current password.
    It calls the ChangePasswordForm class from forms.py.
    Checks if the current password is correct, validate new password.
    Then if new password matchs confirm password field,
    insert it to the database.
    '''
    # prevents guest users from viewing the form
    if 'username' not in session:
        flash('You must be logged in to change password!')
    users = mongo.db.users
    form = ChangePasswordForm()
    username = users.find_one({'username': session['username']})['username']
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get("confirm_new_password")
    if form.validate_on_submit():
        # checks if current password matches existing password in database
        if check_password_hash(users.find_one({'username': username})
                               ['password'], old_password):
            # checks if new passwords match
            if new_password == confirm_password:
                # update the password and redirect to the settings page
                users.update_one({'username': username},
                                 {'$set': {'password': generate_password_hash
                                           (request.form['new_password'])}})
                flash("Success! Your password was updated.")
                return redirect(url_for('profile', username=username))
            else:
                flash("New passwords do not match! Please try again")
                return redirect(url_for("change_password",
                                        username=session["username"]))
        else:
            flash('Incorrect original password! Please try again')
            return redirect(url_for('change_password',
                                    username=session["username"]))
    return render_template('change_password.html', username=username,
                           form=form)


@app.errorhandler(413)
def fileLarge(e):
    flash("Your file is too big"), 413
    return redirect(url_for('uploads_video'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
