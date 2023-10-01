import os
import random
import string

# Function to generate a random string for file names
def generate_random_string(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

# Function to create a random number of empty .txt files in a directory
def create_random_files(directory, num_files):
    for _ in range(num_files):
        file_name = generate_random_string() + ".txt"
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'w') as f:
            pass

# Specify the number of randomly named files you want to create
num_files_to_create = 10  # Change this number as needed

# Specify the directory where you want to create these files
output_directory = "random_files"

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Generate random number of empty .txt files for each randomly named file
for i in range(num_files_to_create):
    num_empty_files = random.randint(1, 50)  # Change the range as needed
    folder_name = generate_random_string()
    folder_path = os.path.join(output_directory, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    create_random_files(folder_path, num_empty_files)

print(f"Created {num_files_to_create} randomly named folders with random empty .txt files in the '{output_directory}' directory.")