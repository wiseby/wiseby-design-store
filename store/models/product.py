class Product:
    def __init__(self, name, description, price, images = [], id = 0, created = ""):
        self.id = id
        self.created = created
        self.name = name
        self.description = description
        self.price = price
        self.images = images

class Image:
    def __init__(self, id, name, alt_text, created):
        self.id = id
        self.name = name
        self.alt_text = alt_text
        self.created = created