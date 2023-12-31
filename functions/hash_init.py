import os
from helpers import select_random_location, create_hash_file

SOURCE_DIR = os.getcwd()
DESTINATION_DIR = "/media/hardrive1"

print("src = ",SOURCE_DIR)
print("dst = ",DESTINATION_DIR)

"""
locs = [select_random_location(SOURCE_DIR),
         select_random_location(DESTINATION_DIR)]
"""
locs = [select_random_location(SOURCE_DIR),
         DESTINATION_DIR]

hash_locations = create_hash_file(locs)

with open(".env", "w", encoding="utf8") as f:
    f.write(f"SRC_VALIDATION_HASH_LOC = '{hash_locations[0]}'\n")
    f.write(f"DST_VALIDATION_HASH_LOC = '{hash_locations[1]}'")
