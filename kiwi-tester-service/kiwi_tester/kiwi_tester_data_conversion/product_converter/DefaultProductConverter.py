class DefaultProductConverter:
    def __init__(self, decoratee = None):
        self._decoratee = decoratee
    
    def convert(self, product):
        """
        receives a products of type
        ("product_id", ["tag1", "tag2", "tag3"])

        and it will be converted to

        {
            "id": ...,
            "tags": []
        }

        """
        if self._decoratee is not None:
            dataset = self._decoratee.convert(dataset)

        #print("Converting with DefaultProductConverter")
        return {
            "id": product[0],
            "tags": product[1]
        }

    def __getattr__(self, name):
        return getattr(self._decoratee, name)