from task import run_command
from optparse import OptionParser

parser = OptionParser(usage="tran paramater", version="0.1")

parser.add_option("-p","--paramater",dest="paramater",
			help="tran paramater",default="echo \"hello world\"")

(option, args) = parser.parse_args()

command = option.paramater

result = run_command.delay(command)
#print result.get(timeout=1)
print result.state