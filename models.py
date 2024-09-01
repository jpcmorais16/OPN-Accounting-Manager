class Product:
    def __init__(self, cb, supermarket, name, amount: int, shift, type=''):
        self.cb = cb
        self.supermarket = supermarket
        self.name = name
        self.amount = amount
        self.shift = shift
        self.type = type

    def __str__(self):
        return f"cb={self.cb}, name={self.name}, supermarket={self.supermarket}, amount={self.amount}"


class Product_db:
    def __init__(self, cb, name, type='', measurement=0.0):
        self.cb = cb
        self.name = name
        self.type = type
        self.measurement = measurement

    def __str__(self):
        return f"cb={self.cb}, name={self.name}"
