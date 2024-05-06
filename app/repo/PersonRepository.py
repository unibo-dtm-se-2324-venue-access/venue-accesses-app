from app.entities.Person import Person
from app.db.db import DbManager, MySQLDb, QueryType
from app.services.AuthenticationService import AuthenticationService
from app.sql_query.QueryUserAuth import SqlUserAuth

class PersonRepository:
    def __init__(self):
        self.db = DbManager(MySQLDb())

    def get_user_info_auth(self, username: str) -> Person:
        sql = SqlUserAuth.get_user_info_auth()
        params = {"username": username}
        with self.db as db:
            result = db.execute_query(sql, (username,), fetchall=True, query_type=QueryType.GET)
        if result:
            return Person(**result[0])
        return None

    def get_encrypted_password(self, password: str) -> dict:
        hashed_pw = AuthenticationService.hash_password(password=password)
        return hashed_pw
    
    def check_password(self, stored_password: str, password: str):
        return AuthenticationService.check_password(stored_hash=stored_password, provided_password=password)
