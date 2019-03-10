import os
import sys
from pprint import pprint

from nano3d.viewer import main

os.chdir(os.path.dirname(os.path.realpath(__file__)))
print('Working dir: {}'.format(os.getcwd()))
print('sys.path:')
pprint(sys.path)
main()

