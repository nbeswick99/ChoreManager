from flask import flash 
from flask_app.config.pymysqlconnection import MySQLConnection
from flask_app.models.child import Child
from flask_app.models.chore import Chore
from flask_app.models.reward import Reward
from flask_app import db_name
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')
class Parent:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.email = data["email"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.children = []
        self.chores = []

    #Create Parent User
    @classmethod
    def create_parent(cls, data):
        query = """
                INSERT INTO parents (email, first_name, last_name, password)
                VALUES (%(email)s, %(first_name)s, %(last_name)s, %(password)s)
                """
        results = MySQLConnection(db_name).query_db(query, data)
        return results

    #Get one parent for login 
    @classmethod
    def get_one_by_email(cls, user):
        query = """
                SELECT *
                FROM parents
                WHERE email = %(email)s;
                """
        data = {
            "email": user["email"]
        }
        results = MySQLConnection(db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    #Might not need this 
    @classmethod
    def get_one_by_id(cls, user):
        query = """
                SELECT *
                FROM parents
                WHERE id = %(id)s;
                """
        data = {
            "id": user
        }
        results = MySQLConnection(db_name).query_db(query, data)
        return cls(results[0])
    
    # @classmethod
    # def get_parent_with_children(cls, parent_id):
    #     data = {
    #         "id": parent_id
    #     }
    #     query = """
    #             select * from children
    #             LEFT JOIN parents ON parent_id = parents.id
    #             WHERE parent_id = %(id)s;
    #             """
    #     results = MySQLConnection(db_name).query_db(query, data)
    #     if results:
    #         parent_dict = {
    #             "id": results[0]["parents.id"],
    #             "email": results[0]["email"],
    #             "first_name": results[0]["parents.id"],
    #             "last_name": results[0]["last_name"],
    #             "password": results[0]["parents.password"],
    #             "created_at": results[0]["parents.created_at"],
    #             "updated_at": results[0]["parents.updated_at"]
    #         }
    #         parent = Parent(parent_dict)
    #         for each_child in results:
    #             child = Child(each_child)
    #             parent.children.append(child)
    #         return parent
    #     else:
    #         parent = Parent.get_one_by_id(parent_id)
    #         return parent

    #Allow Parent to get all chores
    @classmethod
    def all_chores_by_parent_ID(cls, parent_id):
        data = {
            "id": parent_id
        }
        query = """
                select * from chores
                LEFT JOIN parents ON parent_id = parents.id
                WHERE parent_id = %(id)s;
                """
        results = MySQLConnection(db_name).query_db(query, data)
        if results:
            parent_dict = {
                "id": results[0]["parents.id"],
                "first_name": results[0]["first_name"],
                "last_name": results[0]["last_name"],
                "created_at": results[0]["parents.created_at"],
                "updated_at": results[0]["parents.updated_at"]
            }
            parent = Parent(parent_dict)
            for each_chore in results:
                chore = cls(each_chore)
                parent.chores.append(chore)
            return parent
        else:
            parent = Parent.get_one_by_id(parent_id)
            return parent

    #Allows parent to add chore to a child
    @classmethod
    def add_chore_to_child(cls, data):
        query = """
                INSERT INTO chores_has_children (chore_id, child_id)
                VALUES (%(chore_id)s, %(child_id)s);
                """
        results = MySQLConnection(db_name).query_db(query, data)
        return results
    
    #Validation for Parents
    @staticmethod
    def validate_reg(user):
        is_valid = True
        if Parent.get_one_by_email(user): 
            flash("Email is already taken", "parent_register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "parent_register")
            is_valid = False
        if not NAME_REGEX.match(user["first_name"]):
            flash("Invalid Characters in first name", "parent_register")
            is_valid = False
        if len(user["first_name"]) < 2:
            flash("First name must be at least two letters", "parent_register")
            is_valid = False
        if not NAME_REGEX.match(user["last_name"]):
            flash("Invalid Characters in last name", "parent_register")
            is_valid = False
        if len(user["last_name"]) < 2:
            flash("Last name must be at elast two letters", "parent_register")
            is_valid = False
        if not PASSWORD_REGEX.match(user["password"]):
            flash("Password must be at least 8 characters, and must contain one lower case letter, one upper case letter and one of the following special character '# ? ! @ $ % ^ & * -'", "parent_register")
            is_valid = False
        if not user["password"] == user["confirm_password"]:
            flash("Passwords did not match", "parent_register")
            is_valid = False
        return is_valid