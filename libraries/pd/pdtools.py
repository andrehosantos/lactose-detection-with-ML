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
            file_list (dict): A dictionary of files organized by units and concentrations.
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
        for file in files_list:
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

    def create_dataframes(self, drop_columns: list) -> None:
        """
        Create multiple dataframes from a dictionary of files.

        Args:
            drop_columns (list): A list of column indices to drop from the dataframes.
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
                        self.dataframes[units][concentration].append(data_frame)
                else:
                    self.dataframes[units][concentration].extend(dfs)

    def concatenate_dataframes(self) -> None:
        """
        Concatenate multiple dataframes.
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
            concatenated (bool): Indicates whether to consider concatenated dataframes.

        Returns:
            dict: A dictionary containing the biggest dataframe for each unit.
        """
        biggest_dataframes = {}

        dataframes = self.concat_dataframes if concatenated else self.dataframes

        for units, concentrations in dataframes.items():
            if units not in biggest_dataframes:
                biggest_dataframes[units] = None
            max_shape = (0, 0)
            for concentration, dfs in concentrations.items():
                for df in dfs:
                    if df.shape > max_shape:
                        max_shape = df.shape
                        biggest_dataframes[units] = df
        return biggest_dataframes

    def groupdf_by(self, dataframes: dict, column: str) -> dict:
        """
        Group dataframes by a specified column.

        Args:
            dataframes (dict): A dictionary of dataframes organized by units and concentrations.
            column (str): The column name to group by.

        Returns:
            dict: A dictionary of grouped dataframes.
        """
        pass
