from abc import ABC,abstractmethod


class UserInterface(ABC):
    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_by_id(self,id):
        pass

    @abstractmethod
    def get_user_by_email(self,email):
        pass

    @abstractmethod
    def update_user(self,user_id,dictionary):
        pass

    @abstractmethod
    def delete_user(self,user):
        pass

    @abstractmethod
    def register_user(self,username,email,password):
        pass

    @abstractmethod
    def add_user_to_database(self,user):
        pass