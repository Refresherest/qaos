class Database:

    def save(self, key, value):
        raise NotImplementedError

    def load(self, key):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError