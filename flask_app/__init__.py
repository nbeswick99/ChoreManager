from flask import Flask 
app = Flask(__name__)

db_name = "chore_manager_schema"
app.secret_key = "ooga booga"