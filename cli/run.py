import sys
from os.path import dirname

sys.path.append(dirname(dirname(__file__)))

import cli

cmd = cli.Command(sys.argv[1])
cmd.run()
