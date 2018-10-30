
import os

def _create_file(source,content,right):
    file = open(source,right)
    file.write(content)
    file.close()

def _create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
