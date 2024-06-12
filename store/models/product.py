class Product:
    def __init__(self, name, description, price, images = [], id = 0, created = ""):
        self.id = id
        self.created = created
        self.name = name
        self.description = description
        self.price = price
        self.images = images

class Image:
    def __init__(self, image):
        self.id = image['id']
        self.name = image['name']
        self.source = image['source']
        self.alt_text = image['alt_text']
        self.created = image['created']