import os


def get_files(folder_path: str = './', ext: str = '.txt') -> dict:
    """
    Return a dictionary of all filenames and their corresponding paths given a folder name to look into.

    Args:
        folder_path (str): relative folder path (default='./')

    Returns:
        dictionary: A nested dictionary of the form {unit: {concentration: [list of file paths]}}
    """
    files_dict = {}
    for root, dirs, files in os.walk(folder_path):
        if len(files) > 0:
            folder_parts = root.split(os.sep)
            concentration = folder_parts[-1]
            units = folder_parts[-2]
            files_list = [os.path.join(root, file) for file in files if file.endswith(ext)]
            if units not in files_dict: 
                files_dict[units] = {}
            if concentration not in files_dict[units]:
                files_dict[units][concentration] = []
            files_dict[units][concentration].extend(files_list)
    return files_dict