import os
import pandas as pd

from utils.FileHandler import get_files


class Dataframe:
    """
    Custom DataFrame class with additional functionality.
    """

    def __init__(self, file_list: dict, sep: str = '\t') -> None:
        """
        Initialize the Dataframe object.

        Args:
            file_list (str): The path to the file or directory.
            sep (str): The delimiter used in the file (default is '\t' for tab-separated files).
        """
        self.file_list = file_list
        self.sep = sep
        self.dataframes = {}
        self.concat_dataframes = {}

    def import_data(self, files_list: list) -> list:
        """
        Import data from a list of file paths.

        Args:
            files_list (list): A list of file paths.

        Returns:
            list: A list of Pandas DataFrames.
        """
        data = []
        for file in files_list[0]:
            data.append(pd.read_csv(file, sep=self.sep))
        return data

    def drop_columns(self, df: pd.DataFrame, indices: list = []) -> pd.DataFrame:
        """
        Drop columns from a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to drop columns from.
            indices (list): A list of column indices to drop (default is an empty list).

        Returns:
            pd.DataFrame: The DataFrame with dropped columns.
        """
        return df.drop(df.columns[indices], axis=1)

    def create_dataframes(self, drop_columns: list) -> dict:
        """
        Create multiple dataframes from a dictionary of files.

        Args:
            files_list (dict): A dictionary of files organized by units and concentrations.
            drop_indices (list): A list of column indices to drop from the dataframes.

        Returns:
            dict: A dictionary of dataframes organized by units and concentrations.
        """
        for units, concentrations in self.file_list.items():
            if units not in self.dataframes:
                self.dataframes[units] = {}
            for concentration, files_list in concentrations.items():
                dfs = self.import_data(files_list)
                if concentration not in self.dataframes[units]:
                    self.dataframes[units][concentration] = []
                if drop_columns:
                    for i, data_frame in enumerate(dfs):
                        data_frame = self.drop_columns(data_frame, drop_columns)
                        self.dataframes[units][concentration].append(data_frame)  # Append individual DataFrame
                else:
                    self.dataframes[units][concentration].extend(dfs)  # Append the entire list of DataFrames

    def concatenate_dataframes(self) -> dict:
        """
        Concatenate multiple dataframes.

        Args:
            pd_dataframes (dict): A dictionary of dataframes organized by units and concentrations.

        Returns:
            dict: A dictionary of concatenated dataframes organized by units and concentrations.
        """
        for units, concentrations in self.dataframes.items():
            if units not in self.concat_dataframes:
                self.concat_dataframes[units] = {}
            for concentration, dfs in concentrations.items():
                if concentration not in self.concat_dataframes[units]:
                    self.concat_dataframes[units][concentration] = []
                concat_dfs = pd.concat(dfs, axis=0)
                self.concat_dataframes[units][concentration].append(concat_dfs)

    def get_biggest_dataframe(self, concatenated: bool = False) -> dict:
        """
        Get the biggest dataframe from a dictionary of dataframes.

        Args:
            dataframes (dict): A dictionary of dataframes organized by units and concentrations.

        Returns:
            pd.DataFrame: The biggest dataframe.
        """
        biggest_shape = None
        biggest_df = {}

        dataframes = self.dataframes
        if concatenated:
            dataframes = self.concat_dataframes
        biggest_dataframes = {}
    
        for units, concentrations in dataframes.items():
            if units not in biggest_dataframes:
                biggest_dataframes[units] = None
            biggest_df = None
            max_shape = (0,0)
            for concentration, dfs in concentrations.items():
                for df in dfs:
                    if df.shape > max_shape:
                        max_shape = df.shape
                        biggest_dataframes[units] = df
        return biggest_dataframes
    
    def groupdf_by(self, dataframes: dict, column: str) -> dict:
        pass


# """
# This is the original code. It was changed for bugs correction
# and improvements by GPT-3.5-turbo model using OpenAI API.
# The docstrings were generated # in the same way.
# """

# from dataclasses import dataclass
# import pandas as pd
    

# class Dataframe(pd.DataFrame):
#     def __init__(self, file_list: str = './', sep: str = '\t') -> None:
#         super().__init__()
#         self.file_list = file_list
#         self.sep = sep
#         self.dataframes = {}
    
#     def import_data(self, files_list: list) -> list:
#         data = []
#         for file in files_list[0]:
#             data.append(pd.read_csv(file, sep=self.sep))
#         return data
    
#     def drop_columns(self, df: pd.DataFrame, indices: list = []) -> list:
#         """
        
#         """
#         columns = list(df.columns)
#         columns_to_drop = [columns[i] for i in indices]
#         dropped_df = df.drop(columns_to_drop, axis=1, inplace=True)
#         return dropped_df
        
#     def create_dataframes(self, files_list: dict, drop_indices: list) -> dict:
#         """
#         Generate a new pandas dataframe from a passed fully-qualified filename
#         Returns:
#             dataframe: Two-dimensional table
#         """
#         dataframes = {}
#         for units, concentrations in files_list.items():
#             if units not in dataframes:
#                 dataframes[units] = {}
#             for concentration, files in concentrations.items():
#                 dfs = self.import_data(files)
#                 if concentration not in dataframes[units]:
#                     dataframes[units][concentration] = []
#                 for df in dfs:
#                     self.drop_columns(df, drop_indices)
#                     dataframes[units][concentration].append(df)
#         return dataframes

#     def concatenate_dataframes(self, pd_dataframes: pd.DataFrame) -> pd.DataFrame:
#         """Concatenate two or more pandas dataframes

#         Returns:
#             pd.DataFrame: Concatenated dataframe
#         """
#         concat_dataframes = {}
#         for units, concentrations in pd_dataframes.items():
#             if units not in concat_dataframes:
#                 concat_dataframes[units] = {}
#             for concentration, dfs in concentrations.items():
#                 if concentration not in concat_dataframes[units]:
#                     concat_dataframes[units][concentration] = []
#                 concat_dfs = pd.concat(dfs, axis=0)
#                 concat_dataframes[units][concentration].append(concat_dfs)
#         return concat_dataframes


#     def concatenate_by_folder(self, files_folders: tuple) -> pd.DataFrame:
#         """Concatenate multiple files in a folder .

#         [extended_summary]

#         Args:
#             files_folders (tuple): [description]

#         Returns:
#             pd.DataFrame: [description]
#         """
#         df_list = []
#         for _, filelist in files_folders:
#             dataframes = []
#             for file in filelist:
#                 dataframe = self.create_dataframe(file)
#                 dataframes.append(dataframe)
#             conc_df = self.concatenate_dataframes(dataframes)
#             df_list.append(conc_df)