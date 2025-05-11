from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Decorator to ensure that a user is logged in before accessing a route.
def login_required(f):
    """
    A decorator to enforce login requirements for specific routes.
    - If the user is logged in, the route is executed.
    - If not, the user is redirected to the login page with an error message.
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        # check if user is logged in
        if "user_id" in session:
            return f(*args, **kwargs)
        else:
            # Redirect to login if not logged in
            flash("You need to login first", "error")
            return redirect("/login")
    return wrap

# Initialize the Flask app
app = Flask(__name__)

# Configure session to use the filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to the SQLite database
db = SQL("sqlite:///todo.db")

# Route for the home page (task list)
@app.route("/")
@login_required
def index():
    """
    Displays the home page with the list of tasks for the logged-in user.
    - Fetches tasks from the database for the current user.
    - Renders the 'index.html' template with the task data.
    """
    user_id = session["user_id"]
    tasks = db.execute("SELECT * FROM tasks WHERE user_id = ?", user_id)
    return render_template("index.html", tasks=tasks)

# Route to add a new task
@app.route("/add", methods=["POST"])
@login_required
def add_task():
    """
    Handles adding a new task for the logged-in user.
    - Validates that the task description is not empty.
    - Inserts the task into the database.
    - Redirects back to the home page with a success or error message.
    """
    task = request.form.get("task")
    if not task:
        flash("Task cannot be empty.", "error")
        return redirect("/")

    db.execute("INSERT INTO tasks (user_id, description) VALUES (?, ?)", session["user_id"], task)
    flash("Task added successfully!", "success")
    return redirect("/")

# Route to toggle task completion
@app.route("/complete/<int:task_id>", methods=["POST"])
@login_required
def complete_task(task_id):
    """
    Toggles the completion status of a task.
    - Updates the 'completed' field in the database for the specified task.
    - Redirects back to the home page with a success message.
    """
    db.execute("UPDATE tasks SET completed = NOT completed WHERE id = ? AND user_id = ?", task_id, session["user_id"])
    flash("Task status updated!", "success")
    return redirect("/")

# Route to edit a task
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    """
    Handles editing a task's description.
    - GET: Fetches the task details and displays the edit form.
    - POST: Updates the task description in the database.
    """
    if request.method == "GET":
        task = db.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", task_id, session["user_id"])
        if not task:
            flash("Task not found.", "error")
            return redirect("/")
        return render_template("edit.html", task=task[0])

    if request.method == "POST":
        new_description = request.form.get("description")
        db.execute("UPDATE tasks SET description = ? WHERE id = ? AND user_id = ?", new_description, task_id, session["user_id"])
        flash("Task updated successfully!", "success")
        return redirect("/")

# Route to delete a task
@app.route("/delete/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    """
    Deletes a task from the database.
    - Removes the task for the logged-in user based on the task ID.
    - Redirects back to the home page with a success message.
    """
    db.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", task_id, session["user_id"])
    flash("Task deleted successfully!", "success")
    return redirect("/")

# Route to register a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Handles user registration.
    - GET: Displays the registration form.
    - POST: Validates input, hashes the password, and stores the user in the database.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_pw = request.form.get("confirm_pw")

        # Check for missing fields
        if not username or not password or not confirm_pw:
            flash("All fields are required.", "error")
            return redirect("/register")

        # If passwords don't match
        if password != confirm_pw:
            flash("Passwords do not match.", "error")
            return redirect("/register")

        # Improve password validation
        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "error")
            return redirect("/register")

        # Check if username already exists
        row = db.execute("SELECT * FROM users WHERE username = ?", username)
        if row:
            flash("Username already taken.", "error")
            return redirect("/register")

        # Hash password and store the new user in the database
        hash_pw = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pw)

        flash("Registration successful! Please log in.", "success")
        return redirect("/login")

    return render_template("register.html")

# Route to log in a user
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user login.
    - GET: Displays the login form.
    - POST: Authenticates the user by verifying their username and password.
    """

    # Clear the session only if the user is already logged in
    if "user_id" in session:
        session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check for missing fields
        if not username or not password:
            flash("Please enter both fields.", "error")
            return redirect("/login")

        # Check if the username exists
        row = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(row) != 1 or not check_password_hash(row[0]["hash"], password):
            flash("Invalid username or password.", "error")
            return redirect("/login")

        # If the login is successful, store the user’s ID in the session and redirect them to the task list page
        session["user_id"] = row[0]["id"]
        return redirect("/")

    return render_template("login.html")

# Route to log out a user
@app.route("/logout")
def logout():
    """
    Logs out the current user.
    - Forget the user and Send him back to the login page
    """
    session.clear()
    flash("You have been logged out.", "success")
    return redirect("/login")
    
