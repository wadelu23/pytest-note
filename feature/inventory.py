
class InvalidQuantityException(Exception):
    pass


class NoSpaceException(Exception):
    pass


class ItemNotFoundException(Exception):
    pass


class Inventory:
    def __init__(self, limit=100):
        self.limit = limit
        self.total_items = 0
        self.stocks = {}

    def add_new_stock(self, name, price, quantity):
        if quantity <= 0:
            raise InvalidQuantityException(
                'Cannot add a quantity of {}. All new stocks must have at least 1 item'.format(quantity))
        if self.total_items + quantity > self.limit:
            remaining_space = self.limit - self.total_items
            raise NoSpaceException(
                'Cannot add these {} items. Only {} more items can be stored'.format(quantity, remaining_space))

        self.stocks[name] = {
            'price': price,
            'quantity': quantity
        }
        self.total_items += quantity

    def remove_stock(self, name, quantity):
        if quantity <= 0:
            raise InvalidQuantityException(
                f'Cannot remove a quantity of {quantity}. Must remove at least 1 item')
        if name not in self.stocks:
            raise ItemNotFoundException(
                f'Could not find {name} in our stocks. Cannot remove non-existing stock')
        if self.stocks[name]['quantity'] - quantity <= 0:
            raise InvalidQuantityException(
                f'Cannot remove these {quantity} items. Only {self.stocks[name]["quantity"]} items are in stock')

        self.stocks[name]['quantity'] -= quantity
        self.total_items -= quantity
