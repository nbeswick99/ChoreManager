from flask import render_template, redirect, request, session, flash
from flask_app import app 
from flask_app.models.chore import Chore
from flask_app.models.parent import Parent

@app.route("/parent/<int:parent_id>/chores")
def chores(parent_id):
    parent_with_chores = Chore.all_chores_with_parents(parent_id)
    return render_template("chore_crud/chore.html", parent = parent_with_chores)

@app.route("/parent/<int:parent_id>/add/chore")
def add_chore(parent_id):
    parent = Parent.get_one_by_id(parent_id)
    return render_template("chore_crud/add_chore.html", parent = parent)

@app.route("/parent/<int:parent_id>/add/chore/process", methods=["POST"])
def process_chore(parent_id):
    print(request.form)
    if not Chore.validate_chore(request.form):
        return redirect(f"/parent/{parent_id}/add/chore")
    chore = Chore.create_chore(request.form)
    return redirect(f"/parent/{parent_id}/chores")

@app.route("/parent/<int:parent_id>/chore/<int:chore_id>")
def chore_details(parent_id, chore_id):
    chore = Chore.get_one_by_id(chore_id)
    return render_template("chore_crud/chore_details.html", chore = chore, parent_id = parent_id)

@app.route("/parent/<int:parent_id>/chore/<int:chore_id>/edit")
def chore_edit(parent_id, chore_id):
    chore = Chore.get_one_by_id(chore_id)
    return render_template("chore_crud/chore_edit.html", parent_id = parent_id, chore = chore)

@app.route("/parent/<int:parent_id>/chore/<int:chore_id>/edit/process", methods = ["POST"])
def chore_edit_process(parent_id, chore_id):
    if not Chore.validate_chore(request.form):
        return redirect(f"/parent/{parent_id}/chore/{chore_id}/edit")
    edited_chore = Chore.edit_chore(chore_id, request.form)
    return redirect(f"/parent/{parent_id}/chore/{chore_id}")

@app.route("/parent/<int:parent_id>/chore/<int:chore_id>/delete", methods = ["POST"])
def chore_delete(parent_id, chore_id):
    Chore.delete_chore(chore_id)
    return redirect(f"/parent/{parent_id}/chores")