import sys
from os.path import dirname

sys.path.append(dirname(dirname(__file__)))

from command import Command

cmd = Command(sys.argv[1])
cmd.run()
