import os
import pandas as pd


class Dataframe:
    """
    Custom DataFrame class with additional functionality.
    """

    def __init__(self, file_path: str = './', sep: str = '\t') -> None:
        """
        Initialize the Dataframe object.

        Args:
            file_path (str): The path to the file or directory.
            sep (str): The delimiter used in the file (default is '\t' for tab-separated files).
        """
        self.file_path = file_path
        self.sep = sep

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

    def create_dataframes(self, files_list: dict, drop_indices: list) -> dict:
        """
        Create multiple dataframes from a dictionary of files.

        Args:
            files_list (dict): A dictionary of files organized by units and concentrations.
            drop_indices (list): A list of column indices to drop from the dataframes.

        Returns:
            dict: A dictionary of dataframes organized by units and concentrations.
        """
        dataframes = {}
        for units, concentrations in files_list.items():
            if units not in dataframes:
                dataframes[units] = {}
            for concentration, files in concentrations.items():
                dfs = self.import_data(files)
                if concentration not in dataframes[units]:
                    dataframes[units][concentration] = []
                for data_frame in dfs:
                    data_frame = self.drop_columns(data_frame, drop_indices)
                    dataframes[units][concentration].append(data_frame)
        return dataframes

    @staticmethod
    def concatenate_dataframes(pd_dataframes: dict) -> dict:
        """
        Concatenate multiple dataframes.

        Args:
            pd_dataframes (dict): A dictionary of dataframes organized by units and concentrations.

        Returns:
            dict: A dictionary of concatenated dataframes organized by units and concentrations.
        """
        concat_dataframes = {}
        for units, concentrations in pd_dataframes.items():
            if units not in concat_dataframes:
                concat_dataframes[units] = {}
            for concentration, dfs in concentrations.items():
                if concentration not in concat_dataframes[units]:
                    concat_dataframes[units][concentration] = []
                concat_dfs = pd.concat(dfs, axis=0)
                concat_dataframes[units][concentration].append(concat_dfs)
        return concat_dataframes

    def concatenate_by_folder(self, files_folders: tuple) -> pd.DataFrame:
        """
        Concatenate multiple files from different folders.

        Args:
            files_folders (tuple): A tuple containing pairs of folder names and file lists.

        Returns:
            list: A list of concatenated dataframes.
        """
        df_list = []
        for _, file_list in files_folders:
            dataframes = []
            for file in file_list:
                dataframe = pd.read_csv(file, sep=self.sep)
                dataframes.append(dataframe)
            conc_df = self.concatenate_dataframes(dataframes)
            df_list.append(conc_df)
        return df_list




# from dataclasses import dataclass
# import pandas as pd
    

# class Dataframe(pd.DataFrame):
#     def __init__(self, file_path: str = './', sep: str = '\t') -> None:
#         super().__init__()
#         self.file_path = file_path
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