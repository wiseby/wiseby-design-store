class Blog:
    def __init__(self, title, body, id = 0, created = ""):
        self.id = id
        self.title = title
        self.body = body
        self.created = created

    
    @staticmethod
    def BuildFromDict(blog):
        return Blog(
            id=blog['id'], 
            title=blog['title'], 
            body=blog['body'],  
            created=blog['created'])
