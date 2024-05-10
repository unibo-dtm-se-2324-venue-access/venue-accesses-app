from calendar import monthrange
from decimal import Decimal
import os
import tempfile
from io import BytesIO
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from datetime import date, datetime
import pandas as pd
from app.db.db import DbManager, MySQLDb, QueryType
from app.dependencies import TokenData
from app.services.AuthenticationService import AuthenticationService
from app.sql_query.Query import QuerySqlMYSQL

class AccessRepository:

    def __init__(self):
        self.db_manager = DbManager(MySQLDb())

    def get_access_by_date(self, date: str):
        sql = QuerySqlMYSQL.get_access_by_date_sql()
        params = (date,)
        with self.db_manager as db:
            return db.execute_query(sql, params)
        
    def get_access_by_employee(self, date: str, current_user: TokenData):
        sql = QuerySqlMYSQL.get_access_by_employee_sql()
        params = (current_user.username,date,date)
        with self.db_manager as db:
            return db.execute_query(sql, params)

    def get_registry(self):
        sql = QuerySqlMYSQL.get_registry_sql()
        with self.db_manager as db:
            return db.execute_query(sql)

    def person_exists(self, row_id: int) -> bool:
        sql = QuerySqlMYSQL.sql_check()
        with self.db_manager as db:
            result = db.execute_query(sql, (row_id,), query_type=QueryType.GET)
        return result[0].get("ex") > 0
 
    def add_person(self, row_id: int, first_name: str, last_name: str, email: str, role: str, hire_date: str, end_date: str, user_password: str):
        sql = QuerySqlMYSQL.sql_add()
        hashed_password = AuthenticationService.hash_password(user_password)
        params = (row_id, first_name, last_name, email, role, hire_date, end_date, hashed_password)
        with self.db_manager as db:
            if db.execute_query(sql, params, query_type=QueryType.INSERT):
                db.commit()

    def update_person(self, row_id: int, first_name: str, last_name: str, email: str, role: str, hire_date: str, end_date: str, user_password: str):
        sql = QuerySqlMYSQL.sql_update()
        hashed_password = AuthenticationService.hash_password(user_password)
        params = (first_name, last_name, email, role, hire_date, end_date, hashed_password, row_id)
        with self.db_manager as db:
            if db.execute_query(sql, params, query_type=QueryType.UPDATE):
                db.commit()

    def delete_person(self, row_id: int):
        sql = QuerySqlMYSQL.sql_delete()
        with self.db_manager as db:
            if db.execute_query(sql, (row_id,), query_type=QueryType.DELETE):
                db.commit()

    def insert_access(self, employee_id: int):
        sql = QuerySqlMYSQL.sql_insert_presence()
        with self.db_manager as db:
            if db.execute_query(sql, (employee_id,), query_type=QueryType.INSERT):
                db.commit()

    def insert_access_manual(self, employee_id: int, timestamp, creator):
        sql = QuerySqlMYSQL.sql_insert_presence_manual()
        params = (employee_id, timestamp, creator)
        with self.db_manager as db:
            if db.execute_query(sql, params, query_type=QueryType.INSERT):
                db.commit()

    def extract_delays(self, date: datetime.date):
        sql = QuerySqlMYSQL.get_delays_sql()  
        params = (date, date)

        with self.db_manager as db:
            try:
                data = db.execute_query(sql, params)
                print(f"Data retrieved: {data}") 
                
                if data:
                    df = pd.DataFrame(data)
                    
                    df['delay_minutes'] = df['delay_minutes'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)

                    excel_path = f"delays_{date.strftime('%m%d%Y')}.xlsx"
                    
                    df.to_excel(excel_path, index=False)
                    
                    print(f"Excel file created at {excel_path}")
                    return excel_path
                else:
                    print("No data found for the given date.")
                    return None
            except Exception as e:
                print(f"An error occurred while extracting delays: {e}")
                return None

    def create_excel_report(self, data):
         #TODO
        pass