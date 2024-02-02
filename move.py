import shutil
import os

# source and destination paths
source_path = '/home/omkar/Desktop/test/abc.txt'
destination_path = '/media/omkar/Windows-SSD/xfsdestination'

shutil.move(source_path, destination_path)

original_directory = os.path.dirname(source_path)
file_name = os.path.basename(source_path)
symlink_path = os.path.join(original_directory, file_name)

if os.path.exists(symlink_path):
    os.remove(symlink_path)

os.symlink(os.path.join(destination_path, file_name), symlink_path)

print(f"File '{file_name}' moved to '{destination_path}' and symlink created at '{symlink_path}'")


