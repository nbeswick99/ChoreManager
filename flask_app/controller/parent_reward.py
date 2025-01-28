from flask import render_template, redirect, request, session, flash
from flask_app import app 
from flask_app.models.reward import Reward
from flask_app.models.parent import Parent

#Rewards Page Parent
@app.route("/parent/<int:parent_id>/rewards")
def all_rewards(parent_id):

    parent_rewards = Reward.get_all_rewards(parent_id)
    return render_template("reward_crud/reward.html", parent = parent_rewards)

#Create Reward Form
@app.route("/parent/<int:parent_id>/add/reward")
def add_chore(parent_id):
    parent = Parent.get_one_by_id(parent_id)

    return render_template("reward_crud/add_reward.html", parent = parent )

#Process Create form
@app.route("/parent/<int:parent_id>/add/reward/process", methods = ["POST"])
def add_chore_process(parent_id):
    
    if not Reward.validate_reward(request.form):
        return redirect(f"/parent/{parent_id}/add/reward")



    Reward.create_reward(request.form)

    return redirect(f"/parent/{parent_id}/rewards")

#Rewards Details Page
@app.route("/parent/<int:parent_id/reward/<int:reward_id>")
def reward_deatils(parent_id, reward_id): 
    reward = Reward.get_one_reward_by_id(reward_id)
    return render_template("reward_crud/reward_details.html")

#Edit form for chores
@app.route("/parent/<int:parent_id>/reward/<int:reward_id>/edit")
def edit_reward(parent_id, reward_id):
    reward = Reward.get_one_reward_by_id(reward_id)
    return render_template("reward_crud/reward_edit", parent_id = parent_id, reward = reward)

@app.route("parent/<int:parent_id>/reward/<int:reward_id/edit/process")
def edit_reward_proess(parent_id, reward_id):

    if not Reward.validate_reward(request.form):
        return redirect(f"/parent/{parent_id}/reward/{reward_id}/edit")
    
    edited_reward = Reward.update_reward(reward_id, request.form)
    return redirect(f"/parent/{parent_id}/reward/{reward_id}")

@app.routee("parent/<int:parent_id>/reward/<int:reward_id>/delete", methods = ["POST"])
def reward_delete (parent_id, reward_id):
    Reward.delete_reward(reward_id)
    return redirect(f"/parent/{parent_id}/rewards")