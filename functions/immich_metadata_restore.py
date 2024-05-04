import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from library.helpers import restore_immich_directories

if __name__ == "__main__":
    var = restore_immich_directories()