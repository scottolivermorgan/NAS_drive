import os
import shutil


def process_directories(input_dir):
    dirs = os.listdir(input_dir)
    # Create the directory
    os.makedirs(input_dir + "/output", exist_ok=True)
    for d in dirs:
        if os.path.isdir(os.path.join(input_dir, d)):
            sub_dir_path = os.path.join(input_dir, d)
            x = os.listdir(sub_dir_path)
            for i in x:
                source_dir = f"{sub_dir_path}/{i}"

                destination_dir = input_dir + "/output/" + f"{d} - {i}"
                try:
                    new_name = destination_dir.split("(")[0].strip()
                    print(f"Copying from {source_dir} to {new_name}")
                    shutil.copytree(source_dir, new_name)
                except:
                    print(f"Copying from {source_dir} to {destination_dir}")
                    shutil.copytree(source_dir, destination_dir)


if __name__ == "__main__":
    org_files = input("Org ebooks? y/n?")
    if org_files == "y":
        input_directory = input(
            "Enter directory, e.g.: /media/HD_1/Media/books/Jacqueline - Copy "
        )
        try:
            process_directories(input_directory)
        except:
            print("Invalid path")
