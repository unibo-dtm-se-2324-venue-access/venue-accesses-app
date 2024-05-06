

from app.entities.Person import Person
from app.repo.PersonRepository import PersonRepository


class PersonModel():

  def __init__(self, dal: PersonRepository = PersonRepository()):
    self.dal = dal

  def get_user_info_auth(self, username: str) -> Person:
    return self.dal.get_user_info_auth(username)
  
  def get_encrypted_password(self, password: str):
    return self.dal.get_encrypted_password(password)

  def check_password(self, stored_password: str, password: str):
    return self.dal.check_password(stored_password=stored_password, password=password)