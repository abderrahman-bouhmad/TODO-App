from flask import Flask, render_template, request, redirect, session
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

db = SQL("sqlite:///todo.db")


# register
@app.route("/register", methods=["GET, POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_pw = request.form.get("confirm_pw")

        # check for missing fields
        if not username or not password or not confirm_pw:
            return "All fields are required."

        # if passwords don't match
        if password != confirm_pw:
            return "Passwords do not match."

        # Checking if username already exists
        row = db.execute("SELECT * FROM users WHERE username = ?", username)
        if row:
            return "Username already taken."

        # hash password and store the new user in the database
        hash_pw = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pw)


        return redirect("/login")

    return render_template("register.html")

# login
@app.route("/login", methods=["GET, POST"])
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
        session["user_id"] = row[0]["if"]
        return redirect("/")

    # Show the login form if the request method is GET
    return render_template("login.html")
