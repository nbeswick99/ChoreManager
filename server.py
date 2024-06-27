from flask_app import app
from flask_app.controller import parents
from flask_app.controller import children
from flask_app.controller import children_users
from flask_app.controller import chores

if __name__ == "__main__":
    app.run(debug=True)