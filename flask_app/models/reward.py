from flask import flash 
from flask_app.config.pymysqlconnection import MySQLConnection
from flask_app import db_name

class Reward: 
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.title = data["title"]
        self.cost = data["cost"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.parent = None
        self.children = []

    #Create Reward
    @classmethod
    def create_reward(cls, data):
        query = """
                INSERT INTO rewards (title, cost, description)
                VALUES (%(titile)s, %(cost)s, %(description)s)
                """
        results = MySQLConnection(db_name).query_db(query, data)
        return results
    
    #Get one by ID
    @classmethod
    def get_one_by_id(cls, reward_id):
        query = """
                SELECT * 
                FROM rewards
                WHERE id = %(id)s
                """
        data = {
            "id": reward_id
        }
        results = MySQLConnection(db_name).query_db(query,data)
        return cls(results[0])
    
    @classmethod 
    def update_reward(cls, reward_id, data):
        updated_form = {
            **data,
            "id": reward_id
        }
        query = """
                UPDATE rewards
                SET title = %(title)s,
                cost = %(cost)s,
                description = %(description)s,
                WHERE rewards.id = %(id)s
                """

        results = MySQLConnection(db_name).query_db(query, updated_form) 
        return results 
    
    @classmethod 
    def delete_reward(reward_id): 
        delete_id = {
            "id": reward_id
        }
        query = """
                DELETE FROM rewards
                WHERE id = %(id)s
                """
        results = MySQLConnection(db_name).query_db(query, delete_id)
        return results

    @staticmethod
    def validate_reward(reward):
        is_valid = True

        return is_valid 
        