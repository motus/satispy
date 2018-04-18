
class Solution(object):

    def __init__(self, success=False, error=False, varmap=None):
        self.stats = {}
        self.success = success
        self.error = error
        if varmap is None:
            varmap = {}
        self.varmap = varmap

    def __getitem__(self, i):
        return self.varmap[i]

    def __repr__(self):
        return "Solution: %s error: %s vars: %s stats: %s" % (
            self.success, self.error, self.varmap, self.stats)
