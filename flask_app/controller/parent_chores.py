from flask import render_template, redirect, request, session, flash
from flask_app import app 
from flask_app.models.chore import Chore
from flask_app.models.parent import Parent

#Chores Page
@app.route("/parent/<int:parent_id>/chores")
def chores(parent_id):

    #Get all shores for parent and pass into template
    parent_with_chores = Parent.all_chores_by_parent_ID(parent_id)
    return render_template("chore_crud/chore.html", parent = parent_with_chores)

#Create Chore Form 
@app.route("/parent/<int:parent_id>/add/chore")
def add_chore(parent_id):

    #Get parent information to pass into chore form 
    parent = Parent.get_one_by_id(parent_id)
    return render_template("chore_crud/add_chore.html", parent = parent)

#Process Create form for chores
@app.route("/parent/<int:parent_id>/add/chore/process", methods=["POST"])
def process_chore(parent_id):

    #Check the form submission against hte validation 
    if not Chore.validate_chore(request.form):
        #redirect back to the chore form if the 
        return redirect(f"/parent/{parent_id}/add/chore")
    chore = Chore.create_chore(request.form)

    #Redirect to Chores home after passing validation 
    return redirect(f"/parent/{parent_id}/chores")

#Parents Details Page
@app.route("/parent/<int:parent_id>/chore/<int:chore_id>")
def chore_details(parent_id, chore_id):
    chore = Chore.get_one_by_id(chore_id)
    return render_template("chore_crud/chore_details.html", chore = chore, parent_id = parent_id)

#Form for parent to edit chore 
@app.route("/parent/<int:parent_id>/chore/<int:chore_id>/edit")
def chore_edit(parent_id, chore_id):

    #Get chore data to edit and send it to the view as well as the parent ID
    chore = Chore.get_one_by_id(chore_id)
    return render_template("chore_crud/chore_edit.html", parent_id = parent_id, chore = chore)

#Process chore edits 
@app.route("/parent/<int:parent_id>/chore/<int:chore_id>/edit/process", methods = ["POST"])
def chore_edit_process(parent_id, chore_id):

    #Run validations before submiting the updated chore 
    if not Chore.validate_chore(request.form):
        #Redirect back to edit form if validations fail 
        return redirect(f"/parent/{parent_id}/chore/{chore_id}/edit")
    
    #Send chore to database and redirect to individual chore
    edited_chore = Chore.update_chore(chore_id, request.form)
    return redirect(f"/parent/{parent_id}/chore/{chore_id}")

#Process the deletion of a chore
@app.route("/parent/<int:parent_id>/chore/<int:chore_id>/delete", methods = ["POST"])
def chore_delete(parent_id, chore_id):
    #Delete chore and redirect to chores home 
    Chore.delete_chore(chore_id)
    return redirect(f"/parent/{parent_id}/chores")