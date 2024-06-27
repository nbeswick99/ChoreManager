from flask import render_template, redirect, request, session, flash
from flask_app import app 
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

@app.route("/child/login")
def child_login():
    return render_template("child_login.html")