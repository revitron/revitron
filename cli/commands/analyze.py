import sys
from os.path import dirname

sys.path.append(dirname(dirname(dirname(__file__))))

import cli

cmd = cli.Command('analyze')
cmd.run()
