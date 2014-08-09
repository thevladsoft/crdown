import os
import sys
import shutil
from distutils.util import strtobool

def yes_no_query(question):
    sys.stdout.write('{} (y/n) '.format(question)),
    while True:
        try:
            return strtobool(raw_input().lower())
        except ValueError:
            print("Please respond with 'y' or 'n'.")

def move_ask_overwrite(src, dest):
    if os.path.exists(dest):
        if yes_no_query("File '{}' already exists. Overwrite file?".format(dest)):
            os.remove(dest)
        else:
            sys.exit('Cancelling operation...')
    shutil.move(src, dest)
