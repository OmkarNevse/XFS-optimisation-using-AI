import os
import shutil

def move_file_back_and_delete_symlink(source_path, destination_path, symlink_path):
    try:
        if os.path.islink(symlink_path):
            os.remove(symlink_path)
            print(f"Removed symlink at '{symlink_path}'")

        if os.path.exists(destination_path):
            # Extract the file name from the destination path
            file_name = os.path.basename(destination_path)
            new_location = os.path.join(source_path, file_name)

            # Copy the file to the original location
            shutil.copy2(destination_path, new_location)
            print(f"Copied file back to '{new_location}'")

            # Remove the original file
            os.remove(destination_path)
        else:
            print(f"Destination path '{destination_path}' does not exist.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Define the paths
source_path = '/home/omkar/Desktop/test/'  # Original source folder
file_name = 'abc.txt'  # The file name you want to move back
destination_path = '/media/omkar/Windows-SSD/xfsdestination/abc.txt'  # The current location of the file
symlink_path = '/home/omkar/Desktop/test/abc.txt'  # The symbolic link path

# Call the function to move the file back and delete the symbolic link
move_file_back_and_delete_symlink(source_path, destination_path, symlink_path)
