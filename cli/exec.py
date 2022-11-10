import sys
from os.path import dirname

sys.path.append(dirname(dirname(__file__)))

from cli import getEnv, getLogFromEnv

env = getEnv()
log = getLogFromEnv().write

log('Running task {}'.format(env.task))

execfile(env.task)