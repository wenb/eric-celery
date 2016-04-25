# encoding=utf8
import sys
from task import run_command
from optparse import OptionParser


class Usage(Exception):
    """docstring for Usage"""
    def __init__(self, msg):
        self.msg = msg


def print_lines(out_put):
    for line in out_put:
        print line.strip()


def main():
    # execute command
    if not sys.argv[1:]:
        print >> sys.stderr, "need a parameter"
    try:
        parser = OptionParser(usage="tran parameter", version="0.1")
        parser.add_option(
            "-p",
            "--parameter",
            dest="parameter",
            help="tran parameter",
            default="echo \"hello world\"")
        (option, args) = parser.parse_args()
        command = option.parameter
        Out_put = run_command.delay(command)
        print_lines(Out_put.get(timeout=100))
    except OptionParser.error, msg:
        raise Usage(msg)
        return 2

if __name__ == '__main__':
    sys.exit(main())
