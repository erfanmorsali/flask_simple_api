class PostErrors:
    def post_not_found(self,id):
        return f"post with id {id} not found"

    def author_not_found(self,id):
        return f"author with id {id} not found"