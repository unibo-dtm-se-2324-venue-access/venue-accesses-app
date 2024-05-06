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
                MIN(ACC.access_time) AS access_time
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
    sub.employee_id,
    sub.first_name,
    sub.last_name,
    sub.access_time,
    GREATEST(TIMESTAMPDIFF(MINUTE, STR_TO_DATE(CONCAT(%s, ' 08:30'), '%Y-%m-%d %H:%i'), sub.access_time), 0) AS DELAY_IN_MINUTES
FROM (
    SELECT 
        EMP.employee_id, 
        EMP.first_name,
        EMP.last_name,
        ACC.access_time,
        @rn := IF(@prev = EMP.employee_id, @rn + 1, 1) AS rn,
        @prev := EMP.employee_id
    FROM venue.MASTER_EMPLOYEES EMP 
    JOIN venue.access_employees ACC ON EMP.employee_id = ACC.employee_id 
    CROSS JOIN (SELECT @rn := 0, @prev := NULL) AS vars
    WHERE ACC.access_time >= STR_TO_DATE(%s, '%Y-%m-%d') 
    AND ACC.access_time < DATE_ADD(STR_TO_DATE(%s, '%Y-%m-%d'), INTERVAL 1 DAY)
    ORDER BY EMP.employee_id, ACC.access_time
) sub
WHERE sub.rn = 1

        """

    @staticmethod
    def sql_update():
        return """        UPDATE venue.MASTER_EMPLOYEES 
        SET first_name = %s, last_name = %s, email = %s, role = %s, hire_date = STR_TO_DATE(%s, '%Y-%m-%d') , end_date = STR_TO_DATE(%s, '%%Y-%%m-%%d') , user_password = %s 
        WHERE employee_id = %s"""
    
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
