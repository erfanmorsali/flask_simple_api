class UserErrors:
    def user_not_found_by_id(self,id):
        return f"user with id {id} not found."

    def user_not_found_by_email(self,email):
        return f"user with email {email} not found."