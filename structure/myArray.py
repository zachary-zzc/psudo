class myArray(list):

    def __init__(self, array=None, *args, **kwargs):
        self.__array = array or []

    def get(self):
        return self.__array

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __iter__(self):
        pass

    def next(self, length):
        pass

    def __hash__(self):
        pass

    def __getattr__(self, attr):
        pass

    def __cmp__(self, obj):
        pass

    def __len__(self):
        return len(self.array)

    def search(self):
        pass

    def insert(self):
        pass

