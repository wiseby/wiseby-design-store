class Product:
    def __init__(self, name, short_description, description, price, images = [], id = 0, created = ""):
        self.id = id
        self.created = created
        self.name = name
        self.description = description
        self.short_description = short_description
        self.price = price
        self.images = images

    @staticmethod
    def BuildFromRequest(request):
        return Product(
            name=request.form['name'], 
            short_description=request.form['short_description'], 
            description=request.form['description'],
            price=request.form['price'],
            images=request.form.getlist('images'))
    
    @staticmethod
    def BuildFromDict(product):
        return Product(
            id=product['id'], 
            name=product['name'], 
            short_description=product['short_description'], 
            description=product['description'], 
            price=product['price'], 
            created=product['created'])

class Image:
    def __init__(self, image):
        self.id = image['id']
        self.name = image['name']
        self.source = image['source']
        self.alt_text = image['alt_text']
        self.created = image['created']