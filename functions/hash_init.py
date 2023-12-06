import os
from helpers import select_random_location, create_hash_file

fp_1 = os.getcwd()
fp_2 = "/media/hardrive1"

locs = [select_random_location(fp_1), select_random_location(fp_2)]
hash_locations = create_hash_file(locs)

with open(".env", "w") as f:
    f.write(f"SRC_VALIDATION_HASH_LOC = '{hash_locations[0]}'\n")
    f.write(f"DST_VALIDATION_HASH_LOC = '{hash_locations[1]}'")
