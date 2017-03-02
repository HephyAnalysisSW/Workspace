
class Dict(dict):
    """
        Converts dictionary into a class with dict keywords as the attributes of the class.
        Not recommended if keys include  non-alphanum characters
    """ 
    def __init__(self,*arg,**kw):
        super(Dict, self).__init__(*arg, **kw)
        self.__dict__ = self


class FakeHeppySample( Dict):
    """
        A stupid class in order to replicate (fake) the Heppy Component Kreator from cmgTuples sample dictionary
    """
    def __init__(self, *args , **kw):
        Dict.__init__(self, *args, **kw)
        self.dataset = self.dbsName
        self.longName = self.name
        self.name = self.cmgName
    def __hash__(self):
        return hash(self.name)

    # weird stuff to make this "dictionary" hashable, http://stackoverflow.com/questions/1151658/python-hashable-dicts
    #def __key(self):
    #    return tuple((k,self[k]) for k in sorted(self))
    #def __hash__(self):
    #    return hash(self.__key())
    #def __eq__(self, other):
    #    return self.__key() == other.__key()

