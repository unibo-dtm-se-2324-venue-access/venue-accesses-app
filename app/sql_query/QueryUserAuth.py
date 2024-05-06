class SqlUserAuth:
    @staticmethod
    def get_user_info_auth():
        """ Retrieve user authentication data, including the hashed password. """
        return f"""
            SELECT
                employee_id,
                email,
                first_name,
                last_name,
                hire_date,
                end_date,
                user_password,
                role
            FROM venue.MASTER_EMPLOYEES
            WHERE email = %s
        """

    @staticmethod
    def update_user_password(username, new_hashed_password):
        """ Update the hashed password for a specific user. """
        return f"""
            UPDATE MASTER_EMPLOYEES
            SET user_password = :new_hashed_password
            WHERE email = %s
        """