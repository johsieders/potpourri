## str8ts
## js 3.4.2010

from searching.searching2 import SearchProblem, searchByFunction, searchByGenerator

blank = ' '
size = 9


class Str8(object):
    """ inner class of Str8tsProblem
        describes a straight
    """

    def __init__(self, row, col, len, s8):
        self.row = row  ## start
        self.col = col  ## start
        self.len = len  ## length
        self.tab = s8.grid  ## enclosing Str8tsProblem

    def orientation(self):
        raise NotImplementedError

    def values(self):
        raise NotImplementedError

    def isempty(self):
        """ Returns true if no field is set """
        return max(self.values()) == 0

    def min(self):
        if self.isempty():
            return 10
        else:
            return min([x for x in self.values() if x > 0])

    def max(self):
        if self.isempty():
            return 0
        else:
            return max([x for x in self.values() if x > 0])

    def __len__(self):
        return self.len

    def __repr__(self):
        return str(self.row) + blank + str(self.col) + blank + \
            str(self.len) + blank + str(self.orientation())

    def rawconstraints(self):
        raise NotImplementedError

    def constraints(self):
        """ Returns all nums on this row not in self in ascending order.
            Contains 10 = size+1 as last constraint
            These nums are illegal in self.
        """
        result = self.rawconstraints()
        result.sort()
        result.append(size + 1)
        return result

    def options(self):
        """ Returns the set of all feasible nums for self """
        if self.isempty():
            last = 0
            result = set()
            for x in self.constraints():
                if x - last > self.len:
                    result |= set(range(last + 1, x))
                last = x
            return result

        else:  ## not empty
            last = 0
            low = self.max() - self.len + 1
            high = self.min() + self.len
            y = self.max()
            for x in self.constraints():
                if last < y < x:  ## occurs exactly once
                    return set(range(max(low, last + 1), min(high, x)))
                else:
                    last = x


class Hor8(Str8):
    def orientation(self):
        return 'h'

    def values(self):
        return self.tab[self.row][self.col: self.col + self.len]

    def rawconstraints(self):
        """ Returns all nums on this row not in self. """
        tmp = range(0, self.col)
        tmp.extend(range(self.col + self.len, size))
        return [abs(self.tab[self.row][j]) for j in tmp \
                if self.tab[self.row][j] not in (0, -size - 1)]


class Ver8(Str8):
    def orientation(self):
        return 'v'

    def values(self):
        return [self.tab[i][self.col] for i in range(self.row, self.row + self.len)]

    def rawconstraints(self):
        """ Returns all nums on this row not in self. """
        tmp = range(0, self.row)
        tmp.extend(range(self.row + self.len, size))
        return [abs(self.tab[i][self.col]) for i in tmp \
                if self.tab[i][self.col] not in (0, -size - 1)]


def parse(s):
    """ read problem from text
        first line skipped
        result = 9x9 array containing initial data and state
        result[i][j] = 0:       empty white field
        result[i][j] = -10:     empty black field (constant)
        0 < result[i][j] < 10:  white digit (constant)
        -9 < result[i][j] < 0:  black digit (constant)
    """
    result = []
    for line in str.splitlines(s)[1:]:
        row = []
        for c in str.split(line):
            if len(c) == 1 and c[0] == '-':  ## empty white field
                row.append(0)
            elif len(c) == 1 and c[0] == 'x':  ## empty black field
                row.append(-10)
            elif len(c) == 1:  ## white digit
                row.append(int(c[0]))
            elif len(c) == 2 and c[0] == 'x':  ## black digit
                row.append(-int(c[1]))
            else:
                raise TypeError
        result.append(row)
    return result


class Str8tsProblem(SearchProblem):
    def __init__(self, input):
        super().__init__()
        self.rows = range(size)
        self.columns = range(size)
        self.numbers = frozenset(range(1, size + 1))
        self.positions = [(i, j) for i in range(size) for j in range(size)]

        if type(input) is Str8tsProblem:
            self.tab = [[input.grid[i][j] for i in self.rows] for j in self.columns]
        elif type(input) is str:
            self.tab = parse(input)
        else:
            raise TypeError

        # constant data
        self.hor8byRow = self.makeHor8byRow()  # all hor8 on row i
        self.ver8byCol = self.makeVer8byCol()  # all ver8 on col j

        # data updated at each step
        self.options = [[None for i in self.rows] for j in self.columns]
        self.updateOptions()
        self.history = '\n'

    def row(self, i):  # 0 <= i <= 8
        return set([abs(self.tab[i][j]) for j in range(size)])

    def col(self, j):  # 0 <= j <= 8
        return set([abs(self.tab[i][j]) for i in range(size)])

    def makeHor8byRow(self):
        """ all horizontal straights by row """
        result = []
        for i in self.rows:
            result.append([])
            inside = False
            for j in self.columns:
                if not inside and self.tab[i][j] >= 0:  ## start of h
                    h = Hor8(i, j, 0, self)
                    inside = True
                elif inside and self.tab[i][j] < 0:  ## end of h
                    h.len = j - h.col  ## length of h
                    result[i].append(h)
                    inside = False
                else:
                    pass
            if inside:  ## close last straight on this row
                h.len = size - h.col
                result[i].append(h)
        return result

    def makeVer8byCol(self):
        """ all vertical straights by column """
        result = []
        for j in self.columns:
            result.append([])
            inside = False
            for i in self.rows:
                if not inside and self.tab[i][j] >= 0:  ## start of v
                    v = Ver8(i, j, 0, self)
                    inside = True
                elif inside and self.tab[i][j] < 0:  ## end of v
                    v.len = i - v.row  ## length of v
                    result[j].append(v)
                    inside = False
                else:
                    pass
            if inside:  ## close last straight on this column
                v.len = size - v.row
                result[j].append(v)
        return result

    def done(self):  ## done iff no zeros left
        return all([self.tab[i][j] != 0 for (i, j) in self.positions])

    def updateOptions(self):
        """ intersect three restrictions:
            each number appears at most once per row and per column
            restrictions from the horizontal straight (i,j) belongs to
            restrictions from the vertical straight (i, j) belongs to
        """
        for i, j in self.positions:
            if self.tab[i][j] != 0:
                self.options[i][j] = set()
            else:
                self.options[i][j] = self.numbers - self.row(i) - self.col(j)
        for i in self.rows:
            for h in self.hor8byRow[i]:
                ops = h.options()
                for j in range(h.col, h.col + h.len):
                    self.options[i][j] &= ops
        for j in self.columns:
            for v in self.ver8byCol[j]:
                ops = v.options()
                for i in range(v.row, v.row + v.len):
                    self.options[i][j] &= ops

    def __iter__(self):
        """ find an empty field offering the least number of options.
            Return this field's options as next steps
            Dead end, if there is a field with no options left.
            Return [] in that case.
        """
        if self.done():
            return iter([])

        i, j, options = min([(i, j, self.options[i][j]) \
                             for i, j in self.positions if self.tab[i][j] == 0], \
                            key=lambda t: len(t[2]))
        if len(options) == 0:
            self.history += '\ndead end at ' + str((i, j))
            return iter([])
        else:
            self.history += '\ntrying ' + str(options) + ' at ' + str((i, j))
            return iter([(i, j, n) for n in options])

    def getState(self):
        state = Str8tsProblem(self)
        state.history = str(self.history)
        return state

    def do(self, step):
        i, j, n = step
        self.tab[i][j] = n  ## set n at (i, j)
        self.updateOptions()

    def undo(self, step):
        i, j, n = step
        self.tab[i][j] = 0  ## clear (i, j)

    def __repr__(self):
        s = ""
        for i in self.rows:
            for j in self.columns:
                n = self.tab[i][j]
                if n == -10:  ## empty black field
                    s += 'x  '
                elif n < 0:  ## black digit
                    s = s + 'x' + str(-n) + ' '
                elif n == 0:  ## empty white field
                    s = s + '-  '
                elif 0 < n < 10:  ## white digit
                    s = s + str(n) + '  '
                else:
                    raise Exception
            s += "\n"
        return s

    def __len__(self):
        return self.history.count('\n')


## Shorthands
def solveByFunction(p):
    """solves the Str8tsProblem given by p"""
    return searchByFunction(Str8tsProblem(p))


def solveByGenerator(p):
    """solves the Str8tsProblem given by p"""
    return searchByGenerator(Str8tsProblem(p))
