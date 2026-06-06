import os
import sys

def to_abs_path(*args):
    return os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),
                        *args)
