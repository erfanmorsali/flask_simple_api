from abc import ABC,abstractmethod

class PostInterface(ABC):

    @abstractmethod
    def get_all_posts(self):
        pass    

    @abstractmethod
    def get_post_by_id(self,id):
        pass
    
    @abstractmethod
    def create_post(self,title,content,user_id):
        pass

    @abstractmethod
    def add_post_to_database(self,post):
        pass

    @abstractmethod
    def delete_post(self,post):
        pass

    @abstractmethod
    def update_post(self,post_id,dictionary):
        pass

    