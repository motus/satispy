
from satispy.io import DimacsCnf
from satispy import Variable, Solution

from satispy.solver.minisat_stats import parse_stats

import os
import sys
from subprocess import check_output, CalledProcessError

from tempfile import NamedTemporaryFile


class Minisat(object):

    COMMAND = 'minisat'

    def __init__(self, command=COMMAND, timeout=None):
        self.command = command
        self.timeout = timeout

    def solve(self, cnf):

        s = Solution()

        with NamedTemporaryFile(mode='w') as infile, \
             NamedTemporaryFile(mode='r') as outfile:

            io = DimacsCnf()

            infile.write(io.tostring(cnf))
            infile.flush()

            try:
                output = check_output(
                    [self.command, infile.name, outfile.name],
                    universal_newlines=True, timeout=self.timeout)
            except CalledProcessError as ex:
                s.success = (ex.returncode == 10)
                output = ex.output

            s.stats = parse_stats(output)

            if not s.success:
                return s

            lines = outfile.readlines()[1:]

            for line in lines:
                varz = line.split(" ")[:-1]
                for v in varz:
                    v = v.strip()
                    value = v[0] != '-'
                    v = v.lstrip('-')
                    vo = io.varobj(v)
                    s.varmap[vo] = value

        return s
