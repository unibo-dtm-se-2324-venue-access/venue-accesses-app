"""
 MIT License
 
 Copyright (c) 2024 Riccardo Leonelli
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
 
"""

class QuerySqlMYSQL:

    @staticmethod
    def sql_insert_presence():
        return "INSERT INTO venue.access_employees (employee_id, access_time) VALUES (%s, CURRENT_TIMESTAMP)"

    @staticmethod
    def sql_insert_presence_manual():
        return "INSERT INTO venue.access_employees (employee_id, access_time, creator_username) VALUES (%s, %s, %s)"

    @staticmethod
    def get_registry_sql():
        return "SELECT * FROM venue.MASTER_EMPLOYEES"

    @staticmethod
    def get_access_by_date_sql():
        return """
            SELECT 
                EMP.employee_id,
                EMP.first_name,
                EMP.last_name,
                GROUP_CONCAT(DATE_FORMAT(ACC.access_time, '%H:%i') ORDER BY ACC.access_time) AS access_time,
                MIN(ACC.access_time) AS enter_time, 
                MAX(ACC.access_time) AS exit_time
            FROM 
                venue.MASTER_EMPLOYEES AS EMP
            JOIN 
                venue.access_employees AS ACC ON EMP.employee_id = ACC.employee_id
            WHERE 
                DATE(ACC.access_time) = %s
            GROUP BY 
                EMP.employee_id, EMP.first_name, EMP.last_name
                """

    @staticmethod
    def get_delays_sql():
        return """
                SELECT 
                    EMP.employee_id,
                    EMP.first_name,
                    EMP.last_name,
                    DATE(ACC.access_time) AS date,
                    TIME_FORMAT(MIN(ACC.access_time), '%H:%i') AS enter_time,
                    CASE
                        WHEN TIME(MIN(ACC.access_time)) > '08:00:00' THEN
                            (TIME_TO_SEC(TIME(MIN(ACC.access_time))) - TIME_TO_SEC('08:00:00')) / 60
                        ELSE
                            0
                    END AS delay_minutes
                FROM 
                    venue.MASTER_EMPLOYEES AS EMP
                JOIN 
                    venue.access_employees AS ACC ON EMP.employee_id = ACC.employee_id
                WHERE 
                    MONTH(ACC.access_time) = MONTH(%s) AND YEAR(ACC.access_time) = YEAR(%s)
                GROUP BY 
                    EMP.employee_id, EMP.first_name, EMP.last_name, DATE(ACC.access_time)
                ORDER BY 
                    EMP.employee_id, DATE(ACC.access_time);

        """

    @staticmethod
    def sql_update():
        return """        
        UPDATE venue.MASTER_EMPLOYEES 
        SET first_name = %s, last_name = %s, email = %s, role = %s, hire_date = STR_TO_DATE(%s, '%Y-%m-%d') , end_date = STR_TO_DATE(%s, '%%Y-%%m-%%d') , user_password = %s 
        WHERE employee_id = %s
        """
    
    @staticmethod
    def sql_add():
        return """INSERT INTO venue.MASTER_EMPLOYEES (employee_id, first_name, last_name, email, role, hire_date, end_date, user_password) 
                  VALUES (%s, %s, %s, %s, %s, STR_TO_DATE(%s, '%Y-%m-%d'), STR_TO_DATE(%s, '%Y-%m-%d'), %s)"""

    @staticmethod
    def sql_check():
        return "SELECT COUNT(*) as ex FROM venue.MASTER_EMPLOYEES WHERE employee_id = %s"

    @staticmethod
    def sql_delete():
        return "DELETE FROM venue.MASTER_EMPLOYEES WHERE employee_id = %s"
    
    @staticmethod
    def get_access_by_employee_sql():
        return """            
            SELECT 
                DATE(ACC.access_time) AS access_date,
                GROUP_CONCAT(DATE_FORMAT(ACC.access_time, '%H:%i') ORDER BY ACC.access_time) AS daily_access_times
            FROM 
                venue.MASTER_EMPLOYEES AS EMP
            JOIN 
                venue.access_employees AS ACC ON EMP.employee_id = ACC.employee_id
            WHERE 
                EMP.email = %s AND
                YEAR(ACC.access_time) = YEAR(%s) AND 
                MONTH(ACC.access_time) = MONTH(%s)
            GROUP BY 
                EMP.employee_id, EMP.first_name, EMP.last_name, DATE(ACC.access_time)
            ORDER BY 
                DATE(ACC.access_time)
            """
    
    @staticmethod
    def get_monthly_report():
        return """

        SELECT 
            employee_id,
            access_time
        FROM 
            venue.access_employees
        WHERE 
            MONTH(access_time) = MONTH(%s) AND YEAR(access_time) = YEAR(%s)
        ORDER BY 
            employee_id, access_time;

"""


    

