from flask import flash 
from flask_app.config.pymysqlconnection import MySQLConnection
from flask_app.models.parent import Parent
from flask_app import db_name

class Chore:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.name = data["name"]
        self.reward = data["reward"]
        self.reoccuring = data["reoccuring"]
        self.needs_confirmed = data["needs_confirmed"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.parent = None

    @classmethod
    def all_chores_with_parents(cls, parent_id):
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
                "email": results[0]["email"],
                "first_name": results[0]["first_name"],
                "last_name": results[0]["last_name"],
                "password": results[0]["password"],
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
        
    @classmethod
    def create_chore(cls, data):
        query = """
                INSERT INTO chores (name, reward, reoccuring, needs_confirmed, description, parent_id)
                VALUES (%(name)s, %(reward)s, %(reoccuring)s, %(needs_confirmed)s, %(description)s, %(parent_id)s)
                """
        results = MySQLConnection(db_name).query_db(query, data)
        return results
    
    @classmethod
    def get_all_chores(cls):
        query = """
                SELECT * 
                From chores;
                """
        results = MySQLConnection(db_name).query_db(query)
        chores = []
        for each in results:
            chore = cls(each)
            chores.append(chore)
        return chores
    
    @classmethod
    def add_chore_to_child(cls, data):
        query = """
                INSERT INTO chores_has_children (chore_id, child_id)
                VALUES (%(chore_id)s, %(child_id)s);
                """
        results = MySQLConnection(db_name).query_db(query, data)
        return results

    @classmethod
    def get_one_by_id(cls, chore_id):
        query = """
                SELECT *
                FROM chores
                WHERE id = %(id)s;
                """
        data = {
            "id": chore_id
        }
        results = MySQLConnection(db_name).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def edit_chore(cls, chore_id, data):
        updated_form = {
            **data,
            "id": chore_id
        }
        query = """
                UPDATE chores
                SET name = %(name)s, 
                reward = %(reward)s,
                reoccuring = %(reoccuring)s,
                needs_confirmed = %(needs_confirmed)s,
                description = %(description)s
                WHERE chores.id = %(id)s;
                """
        results = MySQLConnection(db_name).query_db(query, updated_form)
        return results
    
    @classmethod
    def delete_chore(cls, chore_id):
        updated_id = {
            "id": chore_id
        }
        print(updated_id)
        query = """
                DELETE FROM chores
                WHERE id = %(id)s;
                """
        results = MySQLConnection(db_name).query_db(query, updated_id)
        return results
    
    @staticmethod
    def validate_chore(data):
        is_valid = True
        if not data["name"]:
            is_valid = False
        if not data["reward"]:
            is_valid = False
        if not "needs_confirmed" in data:
            is_valid = False
        if not "reoccuring" in data:
            is_valid = False
        if not data["description"]:
            is_valid = False
        return is_valid