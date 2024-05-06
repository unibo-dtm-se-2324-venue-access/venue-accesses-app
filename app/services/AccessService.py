from app.repo.AccessRepository import AccessRepository


class AccessService:
    def __init__(self):
        self.repository = AccessRepository()

    def get_access_by_date(self, date: str):
        return self.repository.get_access_by_date(date)

    def get_registry(self):
        return self.repository.get_registry()

    def person_exists(self, employee_id: int) -> bool:
        return self.repository.person_exists(employee_id)
    
    def add_person(self, employee_id: int, first_name: str, last_name: str, email: str, role: str, hire_date: str, end_date: str, user_password: str):
        self.repository.add_person(employee_id, first_name, last_name, email, role, hire_date, end_date, user_password)

    def update_person(self, employee_id: int, first_name: str, last_name: str, email: str, role: str, hire_date: str, end_date: str, user_password: str):
        self.repository.update_person(employee_id, first_name, last_name, email, role, hire_date, end_date, user_password)

    def delete_person(self, employee_id: int):
        self.repository.delete_person(employee_id)

    def insert_access(self, employee_id: int):
        self.repository.insert_access(employee_id)

    def insert_access_manual(self, employee_id: int, timestamp, creator):
        self.repository.insert_access_manual(employee_id, timestamp, creator)

    def extract_delays(self, date: str):
        return self.repository.extract_delays(date)
    
    def create_excel_report(self, data):
        return self.repository.create_excel_report(data)

    def empty_excel_response(self):
        return self.repository.empty_excel_response()
