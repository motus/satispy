
from satispy.io import DimacsCnf
from satispy import Variable, Solution

from satispy.solver.minisat_stats import parse_stats

import os
import sys
import subprocess

from tempfile import NamedTemporaryFile


class Minisat(object):

    COMMAND = 'minisat'

    def __init__(self, command=COMMAND, timeout=None):
        self.command = command
        self.timeout = timeout

    def solve(self, cnf):

        s = Solution()

        with NamedTemporaryFile(mode='w') as infile, \
             NamedTemporaryFile(mode='r') as outfile, \
             NamedTemporaryFile(mode='r', delete=False) as statsfile:

            io = DimacsCnf()

            try:
                infile.write(io.tostring(cnf))
                infile.flush()

                ret = subprocess.call(
                    [self.command, infile.name, outfile.name],
                    stdout=statsfile, universal_newlines=True,
                    shell=True, timeout=self.timeout)

                # On Windows, need to close and re-open the file to read it.
                statsfile.close()
                with open(statsfile.name) as minisat_stdout:
                    s.stats = parse_stats(minisat_stdout)

            finally:
                statsfile.close()
                os.remove(statsfile.name)

            if ret != 10:
                return s

            s.success = True

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
