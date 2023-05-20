
import os

class FileFinder:
    """
    Finds all .txt files in a specified folder and its subfolders
    """
    def __init__(self, folder_path: str):
        """
        Initializes the FileFinder class with a specified folder path
        
        :param folder_path: The path to the folder to search for .txt files
        """
        self.folder_path = folder_path
        
    def find_files(self):
        """
        Finds all .txt files in the specified folder and its subfolders and records the folder name, 
        file name, and absolute path for each file found, grouped by the folder name
        """
        txt_files = {}
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                if file.endswith(".txt"):
                    folder_name = os.path.basename(root)
                    file_path = os.path.join(root, file)
                    if folder_name not in txt_files:
                        txt_files[folder_name] = []
                    txt_files[folder_name].append((file, file_path))
        return txt_files

import pandas as pd

class DataFrameProcessor:
    """
    Imports each file from the same folder into a pandas dataframe, drops the first column, and concatenates the dataframes.
    """
    def __init__(self, file_paths):
        """
        Initializes the DataFrameProcessor class with a list of file paths.
        
        Parameters:
        file_paths (list): A list of file paths to import into dataframes.
        """
        self.file_paths = file_paths
        self.dataframes = []
        self.concatenated_dataframe = None
        self.grouped_dataframe = None
        
    def import_dataframes(self):
        """
        Imports each file from the list of file paths into a pandas dataframe and drops the first column.
        """
        for path in self.file_paths:
            df = pd.read_csv(path)
            df = df.iloc[:, 1:]
            self.dataframes.append(df)
            
    def concatenate_dataframes(self):
        """
        Concatenates the dataframes imported from the files.
        """
        self.concatenated_dataframe = pd.concat(self.dataframes)
        
    def group_dataframes(self):
        """
        Groups the data in the concatenated dataframe by the first column.
        """
        self.grouped_dataframe = self.concatenated_dataframe.groupby(self.concatenated_dataframe.columns[0])

import pandas as pd
import numpy as np

class DataFrameGenerator:
    """
    Generates new dataframes based on a Gaussian distribution with the mean and standard deviation calculated in Step 4.
    """
    def __init__(self, dataframe: pd.DataFrame, num_dataframes: int):
        """
        Initializes the DataFrameGenerator class with a pandas dataframe and the number of dataframes to generate.
        
        Parameters:
        dataframe (pandas.DataFrame): The original pandas dataframe to base the new dataframes on.
        num_dataframes (int): The number of new dataframes to generate.
        """
        self.dataframe = dataframe
        self.num_dataframes = num_dataframes
    
    def generate_dataframes(self):
        """
        Generates new dataframes based on a Gaussian distribution with the mean and standard deviation calculated in Step 4 and the same shape as the original dataframe.
        
        Returns:
        list: A list of pandas dataframes generated from the Gaussian distribution.
        """
        mean = self.dataframe.mean()
        std = self.dataframe.std()
        dataframes = []
        for i in range(self.num_dataframes):
            new_dataframe = pd.DataFrame(np.random.normal(mean, std, size=self.dataframe.shape), columns=self.dataframe.columns)
            dataframes.append(new_dataframe)
        return dataframes

class DataExporter:
    """
    Exports the original and generated dataframes to a CSV file named after the folder
    """
    def __init__(self, dataframe, folder_path):
        """
        Initializes the DataExporter class with a pandas dataframe and the folder path
        
        :param dataframe: pandas.DataFrame, The pandas dataframe to export to a CSV file
        :param folder_path: str, The path to the folder to create the CSV file in
        """
        self.dataframe = dataframe
        self.folder_path = folder_path
    
    def export_dataframe(self):
        """
        Exports the pandas dataframe to a CSV file named after the folder
        
        :return: None
        """
        file_name = self.folder_path.split("/")[-1] + ".csv"
        self.dataframe.to_csv(file_name, index=False)

class Main:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def run(self):
        df = DataFrameProcessor(self.folder_path, (100, 10)).process_data()
        for i, gen_df in enumerate(DataFrameGenerator(df, (100, 10)).generate_data()):
            DataExporter(os.path.join(self.folder_path, f"generated_{i+1}"), gen_df).export_data()

init = Main("raw_data")
init.run()