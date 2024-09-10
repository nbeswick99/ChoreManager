from flask import flash 
from flask_app.config.pymysqlconnection import MySQLConnection
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
        self.children = []
        
    #Create Chore 
    @classmethod
    def create_chore(cls, data):
        query = """
                INSERT INTO chores (name, reward, reoccuring, needs_confirmed, description, parent_id)
                VALUES (%(name)s, %(reward)s, %(reoccuring)s, %(needs_confirmed)s, %(description)s, %(parent_id)s)
                """
        results = MySQLConnection(db_name).query_db(query, data)
        return results
    
    #Get All Chores - May not be needed
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

    #Get one chore by chore ID
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
    
    #Update Chore
    @classmethod
    def update_chore(cls, chore_id, data):
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
        delete_id = {
            "id": chore_id
        }
        query = """
                DELETE FROM chores
                WHERE id = %(id)s;
                """
        results = MySQLConnection(db_name).query_db(query, delete_id)
        return results
    
    @staticmethod
    def validate_chore(chore):
        is_valid = True
        if not chore["name"]:
            is_valid = False
        if not chore["reward"]:
            is_valid = False
        if not "needs_confirmed" in chore:
            is_valid = False
        if not "reoccuring" in chore:
            is_valid = False
        if not chore["description"]:
            is_valid = False
        return is_valid