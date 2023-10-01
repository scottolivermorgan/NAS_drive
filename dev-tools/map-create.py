import hashlib
from datetime import datetime

# Get the current datetime
current_datetime = datetime.now()

# Convert the datetime to a string
datetime_str = str(current_datetime)

# Calculate the hash of the datetime string using SHA-256
hash_object = hashlib.sha256(datetime_str.encode())
hash_hex = hash_object.hexdigest()

# Create a text file and write the hash to it
file_name = f"hash_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
with open(file_name, 'w') as file:
    file.write(hash_hex)

print(f"Hash saved to {file_name}")