import types
import models

class Item(types.Resource):
    """Item resource."""

    def get(self):
        items = [item.to_mongo() for item in models.Item.objects.limit(50)]
        return {'items': items}

class Feed(types.Resource):
    """Feed resource."""

    def get(self):

        return {'feeds': [{'headline': 'first'}]}
