class Dependency(object):
    def __init__(self, name, version):
        self.name = name.lower()
        self.version = version

    def __str__(self):
        return '<Dependency %s @ %s>' % (self.name, self.version)

    __repr__ = __str__
