# j.siedersleben
# fasttrack to professional programming
# lesson 9: databases
# 20.11.2020


############################
## list with transactions ##
############################

class talist(list):
    def __init__(self, xs=()):
        list.__init__(self, xs)
        self.before = xs[:]

    def rollback(self):
        self[:] = self.before

    def commit(self):
        self.before[:] = self
