from flask import render_template, redirect, request, session, flash
from flask_app import app 
from flask_bcrypt import Bcrypt 
from flask_app.models.child import Child

bcrypt = Bcrypt(app)

@app.route("/child/login")
def child_login():
    return render_template("child_login.html")

@app.route("/child/login/process", methods=["POST"])
def child_login_process():
    data={
        "email" : request.form["email"]
    }
     
    #Find child user in Database
    child_from_db = Child.get_one_by_email(data)

    if not child_from_db:
        flash("Account does not exist", "child_login")
        return redirect("/")
    
    #checks that email matches but I con't think this is needed. 
    if not child_from_db.email == request.form["email"]:
        flash("Incorrect Email/Password", "child_login")
        return redirect("/")
    
    #Checks Password
    if not bcrypt.check_password_hash(child_from_db.password, request.form['password']):
        flash("Incorrect Email/Password", "child_login")
        return redirect("/")
    
    session['user_id'] = child_from_db.id

    return redirect(f"/child/{child_from_db.id}/dashboard")

@app.route("/child/<int:child_id>")
def child_dashbaord(child_id):
    child = Child.get_child_with_chores(child_id)
    return render_template("child_views/child_dashboard.html", child = child)s