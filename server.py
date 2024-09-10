from flask_app import app
from flask_app.controller import parent_login
from flask_app.controller import parent_children
from flask_app.controller import children_users
from flask_app.controller import parent_chores

if __name__ == "__main__":
    app.run(debug=True)