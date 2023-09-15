## ftl-data warehouse
## ftl: faster than light
## js 05/09/2005

## howMany by Order (time, Produkt, Region)
## howMany((2004, 5),
##         ('Food', 'Obst'), 
##         ('D', 'BY', 'RO'))    

## howMany((2004),
##         ('Food', 'Obst', 'Apfel'), 
##         ('D', 'BY'))         


from numarray import array, ravel, sum


def getFacts(rawfacts):
    rawfacts = iter(rawfacts)
    tmp = []
    for value in rawfacts:
        tmp.append(value)
    return array(tmp)


class DWH(object):
    """
    dimList is a list of all dimensions
    dimDict is a dictionary (key: name of dimension, value: slices)
     
    dimList contains all dimensions in the order given by
    *dimDescriptors. This order is crucial for the correct
    interpretation of facts.
    
    self.facts is a numarray with one axis for each dimension.
    This is the fact table of a data warehouse, that is:
    facts[i1, i2, .. , in] is the value according to facts
    indexed by i1, i2, .. , in (n = number of dimensions).
    """

    def __init__(self, factfactory, *dimensions):
        self.dimList = list(dimensions)  ## dimensions by order
        self.dimDict = {}  ## dimensions by name
        for dim in dimensions:
            self.dimDict[dim.getName()] = dim
        self.facts = factfactory()
        self.facts.shape = [len(dim) for dim in self.dimList]

    def getDimensions(self):
        """
        returns all dimensions of self as a list of strings
        in correct order. Example: ['location', 'product', 'time']
        """
        return [dim.getName() for dim in self.dimList]

    def getLevels(self, dimension):
        """
        returns all levels of this dimension given as a list of strings.
        Examples:
        dwh.getLevels('location') returns ['continent', 'country', 'city']
        dwh.getLevels('time')     returns ['year', 'month', 'day']
        """
        return self.dimDict[dimension].getLevels()

    def getElements(self, dimension, level):
        """
        returns all elements of this level of this dimension
        """
        dim = self.dimDict[dimension]
        return dim.getElements(level)

    def getShape(self):
        return self.facts.shape

    def howMany(self, *args):  ## only by order
        """
        howMany is what data warehouses are all about.
        howMany expects n tuples where n = number of dimensions,
        and where each tuple contains exactly two elements: the level
        within that dimension and the element within that level.
        """
        index = [dim.getSlice(*args[i]) for i, dim in enumerate(self.dimList)]
        values = ravel(self.facts[index])
        return sum(values)
