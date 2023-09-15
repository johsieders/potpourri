## DWH dimensions
## js 10/4/05

from calendar import monthrange
from datetime import date
from types import SliceType


class DWHDimension(object):
    """
    self.name:   this dimension's name
    self.levels: this dimension's levels
    self.slices: a dictionary (key: (el0, el1, .. ), value: slice)
    indicating for each element its slice on the fact table    
        
    ('2005', 'jan', '10'):  slice(n, n+1)                   ## a day at n
    ('2005', 'jan'):        slice(n, n+31)                  ## a month
    ('2005'):               slice(n, n+365)                 ## a year
    ():                     slice(0, number of elements)    ## all of this dimension 
    """

    def __init__(self, name):
        self.name = name

    def getName(self):  ## this dimension's name
        return self.name  ## 'time'

    def getLevels(self):  ## this dimension's levels
        raise NotImplementedError  ## [year, month, day]

    def getElements(self, level):  ## this level's elements
        raise NotImplementedError  ## month => jan, feb, .. dec

    def getSlice(self, *elements):  ## ()               the slice [0:number of elements]
        raise NotImplementedError  ## (2005,)          all of year 2005
        ## (2005, 4)        all of april 2005
        ## (2005, 4, 10)    the one-element-slice for that day

    def __len__(self):  ## the number of elements of this dimension
        return self.getSlice().stop


class DWHSimpleDimension(DWHDimension):
    """
    A dimDescriptor is a list or an iterable of strings.
    The first line contains the name of this dimension.
    The second line contains all levels of this dimension.
    The following lines contain all elements top down.
    At least one level and one element are required.
    A minimal dimDescriptor:
    ['dummy',           ## name is 'dummy'
     'alevel',          ## just one level
     'anelement']       ## just one element
    """

    def __init__(self, dimDescriptor):
        dimDescriptor = iter(dimDescriptor)
        name = dimDescriptor.next()  ## 'Produkt'
        ##        self.name = name
        super(DWHTimeDimension, self).__init__(name)
        self.levels = dimDescriptor.next().split()  ## ['Sparte', 'Gruppe', 'Produkt']
        self.slices = {}
        lastElements = [None] * len(self.levels)  ## [None, None, None]
        n = len(lastElements)

        for count, record in enumerate(dimDescriptor):
            newElements = record.split()
            ## close incomplete slices
            if count > 0:
                for i in range(len(newElements)):
                    self.slices[tuple(lastElements[:n - i])] = \
                        slice(self.slices[tuple(lastElements[:n - i])], count)
            ## update lastElements
            lastElements[n - len(newElements):] = newElements
            ## insert incomplete slices
            for i in range(len(newElements)):
                self.slices[tuple(lastElements[:n - i])] = count

        count += 1
        for item in self.slices.items():
            if type(item[1]) is not SliceType:  ## collect incomplete entries
                self.slices[item[0]] = slice(item[1], count)
        self.slices[()] = slice(0, count)  ## the entry for this dimension

    def getSlice(self, *elements):
        return self.slices[elements]

    def getLevels(self):
        return self.levels

    def getElements(self, level):
        i = self.levels.index(level) + 1
        return [k[:i] for k in self.slices.keys() if len(k) > 0]

    def getName(self):  ## this dimension's name
        return self.name  ## 'time'


class DWHTimeDimension(DWHDimension):
    def __init__(self, firstday, lastday):  ## firstday, lastday are a tuple (year, month, day)
        ## this dimension contains all days from firstday
        ## up to and including lastday
        self.firstday = date(*firstday)
        self.lastday = date(*lastday)
        self.length = (self.lastday - self.firstday).days + 1
        super(DWHTimeDimension, self).__init__('time')
        self.levels = 'year', 'month', 'day'
        self.elements = {'year': range(self.firstday.year, self.lastday.year + 1), \
                         'month': range(1, 13), \
                         'day': range(1, 32)}

    def interval(self, elements):  ## returns as date the first and the last day
        ## of the time interval given by elements

        if len(elements) == 0:  ## the whole thing
            return self.firstday, self.lastday
        elif len(elements) == 1:  ## year is given
            a = elements + (1,)  ## addFun first month
            b = elements + (12,)  ## addFun last month
            return self.interval(a)[0], self.interval(b)[1]
        elif len(elements) == 2:  ## year, month are given
            a = elements + (1,)  ## addFun first day
            b = elements + (monthrange(*elements)[1],)  ## addFun last day
            return self.interval(a)[0], self.interval(b)[1]
        elif len(elements) == 3:  ## year, month and day are given
            d = date(*elements)
            return max(d, self.firstday), min(d, self.lastday)
        else:
            raise TypeError

    def getLevels(self):
        return self.levels

    def getElements(self, level):
        return self.elements[level]

    def getSlice(self, *elements):
        iv = self.interval(elements)
        start = iv[0] - self.firstday  ## number of days to start
        stop = iv[1] - self.firstday  ## number of days to stop
        return slice(start.days, stop.days + 1)

    def __len__(self):
        return self.length
