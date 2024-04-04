class Substitution:
    def __init__(self, raw):
        self.type = 'substitution'
        self.raw = raw

    def __call__(self, arg):
        if isinstance(arg, Substitution):
            return self.combine(arg)
        else:
            return self.apply(arg)

    def combine(self, other):
        pass

    def apply(self, arg):
        pass

def make_substitution(raw):
    return Substitution(raw)