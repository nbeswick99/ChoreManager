from flask import render_template, redirect, request, session, flash
from flask_app import app 
from flask_app.models.parent import Parent
from flask_app.models.child import Child
from flask_app.models.chore import Chore
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

@app.route("/parent/<int:id>/children")
def display_children(id):
    children = Child.get_child_with_chores(id)
    return render_template("child_crud/children.html", parent_id = id, children= children)

@app.route("/parent/<int:parent_id>/child/<int:child_id>/assign/chore", methods = ["POST"])
def assign_chore(parent_id, child_id):
    Chore.add_chore_to_child(request.form)
    print(request.form)
    return redirect (f"/parent/{parent_id}/children")

@app.route("/parent/<int:id>/add/child")
def add_child(id):
    parent = Parent.get_one_by_id(id)
    return render_template("child_crud/add_child.html", parent = parent)

@app.route("/parent/<int:id>/add/child/process", methods=["POST"])
def process_child(id):
    if not Child.validate_reg(request.form):
        return redirect(f"/parent/{id}/add/child")
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    upated_form = {
        **request.form,
        "password" : pw_hash,
    }
    child = Child.create_child(upated_form)
    return redirect(f"/parent/{id}/children")

@app.route("/parent/<int:parent_id>/child/<int:child_id>")
def child_details(parent_id, child_id):
    child = Child.get_one_by_id(child_id)
    chores = Chore.get_all_chores()
    return render_template("child_crud/child_details.html", child = child, parent_id = parent_id, chores = chores)

@app.route("/parent/<int:parent_id>/child/<int:child_id>/edit")
def child_edit(parent_id, child_id):
    child = Child.get_one_by_id(child_id)
    return render_template("child_crud/child_edit.html", parent_id = parent_id, child = child)

@app.route("/parent/<int:parent_id>/child/<int:child_id>/edit/process", methods = ["POST"])
def child_edit_process(parent_id, child_id):
    if not Child.validate_edit(request.form):
        return redirect(f"/parent/{parent_id}/child/{child_id}/edit")
    edited_child = Child.edit_child(child_id, request.form)
    return redirect(f"/parent/{parent_id}/child/{child_id}")

@app.route("/parent/<int:parent_id>/child/<int:child_id>/delete", methods = ["POST"])
def child_delete(parent_id, child_id):
    Child.delete_child(child_id)
    return redirect(f"/parent/{parent_id}/children")
