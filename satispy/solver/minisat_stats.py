
import re

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


def parse_stats(minisat_stdout):
    stats = {}
    for line in minisat_stdout:
        for (name, func, regex) in _RE_MINISAT_STATS:
            match = regex.search(line)
            if match:
                stats[name] = func(match.group(1))
                break
    return stats
