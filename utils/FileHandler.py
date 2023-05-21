import os

@staticmethod
def get_files(dir: str) -> list:
    """
    Retrieve a list of files in a directory and its subdirectories.
    Args:
        dir (str): The directory path.
    Returns:
        list: A list of file paths.
    """
    files_list = []
    for root, _, files in os.walk(dir):
        files_list.extend([os.path.join(root, file) for file in files])
    return files_list