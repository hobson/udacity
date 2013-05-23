class HashTable:
    """What type of keying and hasing is this called?"""
    def __init__(self):
        self.salt = 123456789
        self.num_bins = 1e3
        self.num_values = 0
        self.hash_table = [[] for i in range(self.num_bins) 
        self.wrapped_hashes =[]
        self.values = []
    
    @property
    def load_factor(self):
        float(self.num_values) / self.num_bins

    def index(self, key):
           # very slow hasher for long keys
        return (sum(ord(c) for c in str(key).split()) + self.salt) % self.num_bins

    def __getitem__(self, key):
        bin = self.hash_table[self.index(key)]
        for record in bin:
            if record[0] == key:
                return record[1]
        raise KeyError('The key ' + repr(str(key)) + ' could not be found in the hash table')

    def __setitem__(self, key, value):
        # TODO: is there a way to reuse getitem here to find if the key exists?
        bin = self.hash_table[self.index(key)]
        for record in enumerate(bin):
            if record[0] == key:
                record[1] = value
        self.num_values += 1
        if self.load_factor() > 1.0:
             # make a num_bins setter to expand the deck
             self.num_bins *= 2
            def __getitem__(self, key):
        bin = self.hash_table[self.index(key)]
        for record in bin:
            if record[0] == key:
                return record[1]
        raise KeyError('The key ' + repr(str(key)) + ' could not be found in the hash table')


ht = HashTable
