import os, sys
print(f'> in {__package__}.run, and say:')
if __name__ == '__main__':
    print('This program is being run by itself...\n')
else:
    print('I am being imported from another module...\n')

print(f'os.getcwd: {os.getcwd()}\n'
      f'sys.argv: {sys.argv}\n'
      f'sys.path: {sys.path}')
print('=================')
from pkg1 import moduleA