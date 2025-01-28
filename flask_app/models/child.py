from flask import flash 
from flask_app.config.pymysqlconnection import MySQLConnection
from flask_app.models.chore import Chore
from flask_app.models.reward import Reward
from flask_app import db_name
import re


# Child Regex 
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')

# Child class
class Child:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.username = data["username"]
        self.first_name = data["first_name"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.chores = []
        self.parent = None

    #Create new Child and associate them with a parent
    @classmethod
    def create_child(cls, data):
        query = """
                INSERT INTO children (username, first_name, password, parent_id)
                VALUES (%(username)s, %(first_name)s, %(password)s, %(parent_id)s)
                """
        results = MySQLConnection(db_name).query_db(query, data)
        return results

    @classmethod
    def edit_child(cls, child_id, data):
        updated_form = {
            **data,
            "id": child_id
        }
        query = """
                UPDATE children
                SET username = %(username)s, 
                first_name = %(first_name)s
                WHERE children.id = %(id)s;
                """
        results = MySQLConnection(db_name).query_db(query, updated_form)
        return results
    
    @classmethod
    def delete_child(cls, child_id):
        updated_id = {
            "id": child_id
        }
        print(updated_id)
        query = """
                DELETE FROM children
                WHERE id = %(id)s;
                """
        results = MySQLConnection(db_name).query_db(query, updated_id)
        return results

    @classmethod
    def get_one_by_username(cls, user):
        query = """
                SELECT *
                FROM children
                WHERE username = %(username)s;
                """
        data = {
            "username": user["username"]
        }
        results = MySQLConnection(db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_one_by_id(cls, child_id):
        query = """
                SELECT *
                FROM children
                WHERE id = %(id)s;
                """
        data = {
            "id": child_id
        }
        results = MySQLConnection(db_name).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_child_with_chores(cls, child_id):
        data = {
            "id": child_id
        }

        query = """
                SELECT *
                FROM chores
                LEFT JOIN children ON children_id = children.id
                WHERE child_id = %(id)s
                """
        results = MySQLConnection(db_name).query_db(query, data)

        if results: 

            child_dict = {
                "id": results[0]["children.id"],
                "first_name": results[0]["children.first_name"],
                "username": results[0]["children.username"],
                "password": results[0]["children.password"],
                "created_at": results[0]["children.created_at"],
                "updated_at": results[0]["children.updated_at"],
            }

            child = Child(child_dict)

            for each_chore in results: 
                chore = Chore(each_chore)
                child.chores.append(chore)
            
            return child
        else:
            child = Child.get_one_by_id(child_id)
            return child
    

    @staticmethod
    def validate_reg(user):
        is_valid = True
        if Child.get_one_by_username(user): 
            flash("username is already taken", "child_register")
            is_valid = False
        if not USERNAME_REGEX.match(user['username']): 
            flash("Invalid username address!", "child_register")
            is_valid = False
        if not NAME_REGEX.match(user["first_name"]):
            flash("Invalid Characters in first name", "child_register")
            is_valid = False
        if len(user["first_name"]) < 2:
            flash("First name must be at least two letters", "child_register")
            is_valid = False
        if not PASSWORD_REGEX.match(user["password"]):
            flash("Password must be at least 8 characters, and must contain one lower case letter, one upper case letter and one of the following special character '# ? ! @ $ % ^ & * -'", "child_register")
            is_valid = False
        if not user["password"] == user["confirm_password"]:
            flash("Passwords did not match", "child_register")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_edit(user):
        is_valid = True
        if not USERNAME_REGEX.match(user['username']): 
            flash("Invalid username address!", "child_register")
            is_valid = False
        if not NAME_REGEX.match(user["first_name"]):
            flash("Invalid Characters in first name", "child_register")
            is_valid = False
        if len(user["first_name"]) < 2:
            flash("First name must be at least two letters", "child_register")
            is_valid = False
        return is_valid