import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from library.helpers import restore_jellyfin_metadata, restore_komga_metadata

if __name__ == "__main__":
    restore_jellyfin_metadata()
    restore_komga_metadata()