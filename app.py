from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # check if user is logged in
        if "user_id" in session:
            return f(*args, **kwargs)
        # if not logged in, send them to the login page
        else:
            flash("You need to login first")
            return redirect("/login")
    return wrap

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///todo.db")

@app.route("/")
# add Login Required Decorator Wrapper
@login_required
def index():
    # Grab the current user’s tasks from the database
    user_id = session["user_id"]
    tasks = db.execute("SELECT * FROM tasks WHERE user_id = ?", user_id)
    return render_template("index.html", tasks=tasks)


# register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_pw = request.form.get("confirm_pw")

        # Check for missing fields
        if not username or not password or not confirm_pw:
            flash("All fields are required.")
            return redirect("/register")

        # If passwords don't match
        if password != confirm_pw:
            flash("Passwords do not match.")
            return redirect("/register")

        # Improve password validation
        if len(password) < 8:
            flash("Password must be at least 8 characters long.")
            return redirect("/register")

        # Check if username already exists
        row = db.execute("SELECT * FROM users WHERE username = ?", username)
        if row:
            flash("Username already taken.")
            return redirect("/register")

        # Hash password and store the new user in the database
        hash_pw = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pw)

        flash("Registration successful! Please log in.")
        return redirect("/login")

    return render_template("register.html")

# login
@app.route("/login", methods=["GET", "POST"])
def login():
    # clear existing session, ensuring no previous user is logged in.
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check for missing fields
        if not username or not password:
            flash("Please enter both fields.")
            return redirect("/login")

        # Check if the username exists
        row = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(row) != 1 or not check_password_hash(row[0]["hash"], password):
            flash("Invalid username or password.")
            return redirect("/login")

        # If the login is successful, store the user’s ID in the session and redirect them to the task list page
        session["user_id"] = row[0]["id"]
        return redirect("/")

    # Show the login form if the request method is GET
    return render_template("login.html")

# logout
@app.route("/logout")
def logout():
    # Forget the user and Send him back to the login page
    session.clear()
    return redirect("/login")
