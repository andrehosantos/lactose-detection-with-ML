import os


def get_files(folder_path: str = './', ext: str = '.txt') -> tuple:
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
            files_dict[units][concentration].append(files_list)
    return files_dict

def groupby_folder(files: tuple) -> tuple:
    """List all files grouped within the same folder

    Args:
        files (tuple): a list of all files and folders

    Returns:
        tuple: a list of files grouped by folders
    """
    grouped = {}
    for concentration, dirpath, filepath in files:
        if dirpath not in grouped:
            grouped[dirpath] = []
        grouped[dirpath].append([filepath, dirpath])
    return tuple(grouped.items())
