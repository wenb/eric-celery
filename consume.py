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

#set the paramater

def main():
	if not sys.argv[1:]:
		print >> sys.stderr,"need a paramater"
	try:
		parser = OptionParser(usage="tran paramater", version="0.1")
		parser.add_option("-p","--paramater",dest="paramater",
			help="tran paramater",default="echo \"hello world\"")	
		(option, args) = parser.parse_args()
		command = option.paramater
		result = run_command.delay(command)
		print_lines(result.get(timeout=100))
		#print command
	except OptionParser.error, msg:
		raise Usage(msg)
		return 2

if __name__ == '__main__':
	sys.exit(main())