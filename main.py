import json

fp = "config.json"

# Open and read the config.json file
with open(fp, 'r') as config_file:
    config_data = json.load(config_file)

for object in config_data:
    print(object)