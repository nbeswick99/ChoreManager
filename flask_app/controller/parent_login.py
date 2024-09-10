from flask import render_template, redirect, request, session, flash
from flask_app import app 
from flask_app.models.parent import Parent
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

#Home page/parent login
@app.route("/")
@app.route("/parent/login")
def login(): 
    return render_template("parent_login.html")

#Handle Parent Login Request
@app.route("/parent/login/process", methods=["POST"])
def parent_login_process():
    
    data={
        "email" : request.form["email"]
    }

    #Find parent user in Database
    parent_from_db = Parent.get_one_by_email(data)

    if not parent_from_db:
        flash("Account does not exist", "parent_login")
        return redirect("/")
    
    #checks that email matches but I con't think this is needed. 
    if not parent_from_db.email == request.form["email"]:
        flash("Incorrect Email/Password", "parent_login")
        return redirect("/")
    
    #Checks Password
    if not bcrypt.check_password_hash(parent_from_db.password, request.form['password']):
        flash("Incorrect Email/Password", "parent_login")
        return redirect("/")
    
    session['user_id'] = parent_from_db.id

    return redirect(f"/parent/{parent_from_db.id}/dashboard")

#Register Route for New Parent Users
@app.route("/register")
def register_parent():
    return render_template("register_parent.html")

@app.route("/register/process", methods = ["POST"])
def register_parent_process():

    #Parent Validation
    if not Parent.validate_reg(request.form):
        return redirect("/register")
    
    #Hash Password
    pw_hash = bcrypt.generate_password_hash(request.form["password"])

    #Update form to include the Hashed Password
    updated_form = {
        **request.form,
        "password" : pw_hash,
    }

    #store Parent in Database
    parent = Parent.create_parent(updated_form)

    #store parent in session and redirct to dashboard
    session["Parent_id"] = parent

    return redirect(f"/parent/{parent}/dashboard")

@app.route("/parent/<int:id>/dashboard")
def parent_dashboard(id):

    #get Parent information for dashbaord
    parent = Parent.get_one_by_id(id)

    return render_template("parent_dashboard.html", parent = parent)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")