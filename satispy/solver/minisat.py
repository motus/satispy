
from satispy.io import DimacsCnf
from satispy import Variable, Solution

import re
import sys
import subprocess

from tempfile import NamedTemporaryFile

_RE_MINISAT_STATS = [
    ("variables", int, re.compile(r"^\|\s*Number of variables:\s+(\d+)")),
    ("clauses", int, re.compile(r"^\|\s*Number of clauses:\s+(\d+)")),
    ("parse_time", float, re.compile(r"^\|\s*Parse time:\s+(\d+(?:\.\d+)?) s")),
    ("restarts", int, re.compile(r"^restarts\s*:\s*(\d+)")),
    ("conflicts", int, re.compile(r"^conflicts\s*:\s*(\d+)")),
    ("decisions", int, re.compile(r"^decisions\s*:\s*(\d+)")),
    ("propagations", int, re.compile(r"^propagations\s*:\s*(\d+)")),
    ("conflict_literals", int, re.compile(r"^conflict literals\s*:\s*(\d+)")),
    ("cpu_time", float, re.compile(r"^CPU time\s*:\s*(\d+(?:\.\d+)?) s"))
]


class Minisat(object):

    COMMAND = 'minisat %s %s > %s'

    def __init__(self, command=COMMAND, timeout=None):
        self.command = command
        self.timeout = timeout

    def solve(self, cnf):

        s = Solution()

        with NamedTemporaryFile(mode='w') as infile, \
             NamedTemporaryFile(mode='r') as outfile, \
             NamedTemporaryFile(mode='r') as statsfile:

            io = DimacsCnf()
            infile.write(io.tostring(cnf))
            infile.flush()

            ret = subprocess.call(
                self.command % (infile.name, outfile.name, statsfile.name),
                shell=True, timeout=self.timeout)

            for line in statsfile:
                for (name, func, regex) in _RE_MINISAT_STATS:
                    match = regex.search(line)
                    if match:
                        s.stats[name] = func(match.group(1))
                        break

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
