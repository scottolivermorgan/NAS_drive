import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from library.helpers import (
    activate_logical_volume, 
    mount_logical_volume
    )

if __name__ == "__main__":
    activate_logical_volume('your_volume_group', 'backup_lv1')
    mount_logical_volume('/mnt/backup', 'your_volume_group', 'backup_lv1')
